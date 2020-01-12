import pytest
import logging
import json
import requests
import ast
import time
from utils import get_accounts
import pyotp
import ast

ws_url = 'ws//:trading.xena.exchange/'
trading_url = 'https://trading.xena.exchange/'
base_url = 'https://xena.exchange/'

logging.basicConfig(level=logging.INFO)


# TODO think about no login if its not required
with open("../accounts.json", "r") as read_file:
    data = json.load(read_file)
    accounts = [i for i in data['accounts']]
    sessions = []

    for account in accounts:
        response = requests.post(url=trading_url + '/api/auth/login', json=account['login_data'])
        try:
            jresp = json.loads(response.text)
            logging.info("Login response" + response.text)
        except:

            logging.error('response code is ' + str(response.status_code))
            logging.error('Cant parse json, incorrect response is ' + response.text + '. Login data is' + str(
                account['login_data']))
        sessions.append(
            {
                "login_data": account['login_data'],
                "nonce": jresp['nonce'],
                "cookies": response.cookies,
                "scopes": account['scopes'],
                "accounts": jresp['accounts']
            }
        )

# This shit does not work for python 3.7 and pytest >4.0,need to think about global variables, till the repair
# def pytest_namespace():
#    return {'session': None}

main_fixtures = ['session', 'account', 'account_currency']
session_based_fixtures = {'apikey', 'payment', 'cancel_payment'}


def pytest_generate_tests(metafunc):
    # valid session data
    if 'session' in metafunc.fixturenames:
        test_data = []
        fixtures = 'session'
        active_session_based_fixtures = []
        for session in sessions:
            # if scope of session is valid for certain test
            if any([i for i in ['all', metafunc.function.__name__] if i in session['scopes']]):
                # valid account data for session
                if 'account' in metafunc.fixturenames:
                    fixtures += ', account'
                    for acc in session['accounts']:
                        # valid account currency for account
                        if 'account_currency' in metafunc.fixturenames:
                            fixtures += ', account_currency'
                            # new test data row for each currency
                            # TODO ETH, USDT, BTC should be loaded from config file (enabled spot currencies)
                            for cur in acc.get('currency', 'ETH,USDT,BTC').split(","):
                                test_data.append((session, str(acc['id']), cur))
                        else:
                            # place for fixtures where session and account are needed
                            test_data.append((session, str(acc['id'])))
                else:
                    # place for fixtures where only session is needed
                    active_session_based_fixtures = session_based_fixtures.intersection(metafunc.fixturenames)
                    test_data.append(len(active_session_based_fixtures) and (
                                [session] * (len(active_session_based_fixtures) + 1)) or session)
        # TODO update ids generation
        metafunc.parametrize(
            ','.join([i for i in ['session'] + list(active_session_based_fixtures) + ['account', 'account_currency'] if
                      i in metafunc.fixturenames]),
            test_data, indirect=list(active_session_based_fixtures)
        )
        return

    # invalid account number for spot/margin endpoints
    # TODO Must be updated for negative tests
    if 'negative_account' in metafunc.fixturenames:
        test_data = []
        for session in sessions:
            if any([i for i in ['negative', metafunc.function.__name__] if i in session['scopes']]):

                spot_account = [i['id'] for i in session['accounts'] if i['kind'] == 'Spot'][0]
                margin_account = [i['id'] for i in session['accounts'] if i['kind'] == 'Margin'][0]

                for negative_account in ['-1',
                                         '0',
                                         'nil',
                                         '9999999999999999',
                                         str(spot_account - 10),
                                         str(margin_account - 10),
                                         str(spot_account + 1000000),
                                         str(margin_account + 1000000000)
                                         ]:
                    test_data.append(
                        (session, negative_account)
                    )
        metafunc.parametrize("session, negative_account", test_data)
        return
    return


@pytest.fixture(scope='session', autouse=True)
def init_tests():
    logging.info('Start')
    yield
    logging.info('End')


@pytest.fixture(scope='function')
def login(request):
    account = request.param
    response = requests.post(url=trading_url + '/api/auth/login', json=account['login_data'])
    jresp = json.loads(response.text)
    yield {"login_data": account['login_data'], "nonce": jresp['nonce'],
           "cookies": response.cookies, "accounts": jresp['accounts']}


@pytest.fixture(scope='function')
def payment_ratio():
    response = requests.get(f'{trading_url}/api/common/payment/ratio')
    jresp = json.loads(response.text)
    yield jresp["paymentSettings"][0]['ratios'][0]['ratio']

# TODO
@pytest.fixture(scope='function')
def payment(request, payment_ratio):
    session = request.param
    data = {"quoteAmount": str(round(0.00400000 * float(payment_ratio), 2)),
            "quoteCurrency": "EUR",
            "baseAmount": "0.00400000",
            "baseCurrency": "BTC",
            "language": "ru",
            "ratio": payment_ratio,
            "account": get_accounts(session, kind='Spot')}
    response = requests.post(f'{trading_url}/api/payment/create', headers={'X-Auth-Nonce': session['nonce']},
                             json=data, cookies=session['cookies'])

    yield "id of payment"

    response = requests.get(f'{trading_url}/api/payment/active-payments', headers={'X-Auth-Nonce': session['nonce']},
                            cookies=session['cookies'])

    if response.text != "[]":
        requests.post(f'{trading_url}/api/payment/cancel/0',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])


@pytest.fixture(scope='function')
def cancel_payment(request):
    yield
    session = request.param
    response = requests.get(f'{trading_url}/api/payment/active-payments', headers={'X-Auth-Nonce': session['nonce']},
                            cookies=session['cookies'])
    if response.text != "[]":
        requests.post(f'{trading_url}/api/payment/cancel/<extracted_id>',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])


@pytest.fixture(scope='function')
def apikey(request):
    session = request.param
    response = requests.post(f'{trading_url}/api/auth/apikeys/new',
                             headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'],
                             json={"scopes": ["trading", "transfers"], "accounts": get_accounts(session)})
    apikey = ast.literal_eval(response.text)

    yield apikey

    response = requests.get(f'{trading_url}/api/auth/apikeys', headers={'X-Auth-Nonce': session['nonce']},
                            cookies=session['cookies'])
    if response.text.find(apikey['apiKey']) != -1:
        requests.delete(f'{trading_url}/api/auth/apikeys',
                        headers={'X-Auth-Nonce': session['nonce']},
                        cookies=session['cookies'], json={"apiKey": apikey['apiKey']})


@pytest.fixture(scope='function')
def generate2fa(request):
    # Login
    account = request.param
    response = requests.post(url=trading_url + '/api/auth/login', json=account['login_data'])
    jresp = json.loads(response.text)
    session = {"login_data": account['login_data'], "nonce": jresp['nonce'],
               "cookies": response.cookies, "accounts": jresp['accounts']}

    # Generate secret
    rsp = requests.post(trading_url + '/api/auth/account/' + str(get_accounts(session)[0]) + '/2fa/generate',
                        headers={'X-Auth-Nonce': session['nonce']},
                        cookies=session['cookies'])
    otp_secret = ast.literal_eval(rsp.text)['key']
    logging.info('Get key' + str(otp_secret))

    yield session, otp_secret
    time.sleep(30)
    # Re-login (required if auth2fa set)
    logging.info('Re-login')
    totp = pyotp.TOTP(otp_secret)
    logging.info(totp.now())
    response = requests.post(url=trading_url + '/api/auth/login', json={"email": account['login_data']['email'],
                                                                        "password": account['login_data']['password'],
                                                                        "passcode": totp.now()})
    jresp = json.loads(response.text)
    session = {"login_data": account['login_data'], "nonce": jresp['nonce'],
               "cookies": response.cookies, "accounts": jresp['accounts']}
    # Disable 2fa
    logging.info('Disable 2fa')
    time.sleep(30)
    logging.info(totp.now())
    data = {
        "password": session['login_data']['password'],
        "passcode": totp.now(),
        "authEnabled": False,
        "enabled": False
    }
    rsp = requests.post(trading_url + '/api/auth/account/' + str(get_accounts(session)[0]) + '/2fa/set',
                        headers={'X-Auth-Nonce': session['nonce']}, json=data,
                        cookies=session['cookies'])
    logging.info('2fa disabled ' + str(rsp.text) + "_" + str(rsp.status_code))


class BaseTest:
    pass
