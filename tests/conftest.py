import pytest
import logging
import json
import requests

ws_url = 'ws//:trading.xena.exchange/'
trading_url = 'https://trading.xena.exchange/'
base_url = 'https://xena.exchange/'

logging.basicConfig(level=logging.INFO)

with open("../accounts.json", "r") as read_file:
    data = json.load(read_file)
    accounts = [i for i in data['accounts']]
    sessions = []

    for account in accounts:
        response = requests.post(url=trading_url+'/api/auth/login', json=account['login_data'])
        try:
            jresp = json.loads(response.text)
        except:

            logging.error('response code is ' + str(response.status_code))
            logging.error('Cant parse json, incorrect response is ' + response.text + '. Login data is' + str(account['login_data']))
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
#def pytest_namespace():
#    return {'session': None}
# need to add sessio not for init
#{'X-Auth-Nonce': jresp['nonce'], 'sid': response.cookies['sid']}

def pytest_generate_tests(metafunc):
    # valid account data
    if 'account' in metafunc.fixturenames:
        test_data = []
        for session in sessions:
            if any([i for i in ['all', metafunc.function.__name__] if i in session['scopes']]):
                for acc in session['accounts']:
                     test_data.append(
                         (session, str(acc['id']))
                                      )
        metafunc.parametrize("session, account ", test_data, ids=[i[0]['login_data']['email'] + '_' + i[1] + '_'
                                                                  for i in test_data])
        return
    # invalid account data for spot/margin endpoints
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

class BaseTest:
    pass