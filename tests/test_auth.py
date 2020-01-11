from tests.conftest import logging, trading_url, accounts
from utils import get_accounts
import requests
import pyotp
import pytest


class TestAuthPositive:

    # AUTH
    @pytest.mark.parametrize("login_data", accounts, ids=[i['desc'] for i in accounts])
    def test_post_login(self, login_data):
        response = requests.post(f'{trading_url}/api/auth/login', json=login_data['login_data'])
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_renew(self, session):
        response = requests.post(f'{trading_url}/api/auth/renew',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.skip(reason="all sessions invalidation")
    @pytest.mark.parametrize('login', [i for i in accounts if 'session_changing' in i['scopes']], indirect=True)
    def test_post_logout(self, login):
        response = requests.post(f'{trading_url}/api/auth/logout', headers={'X-Auth-Nonce': login['nonce']},
                               cookies=login['cookies'], json={})
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.parametrize("scopes, count_of_accounts", [(["trading", "transfers", "daccs"], 1),
                                                           (["readOnlyTrading", "readOnlyBalanceOperations"], 3),
                                                           (["daccs"], 6)])
    def test_post_new_apikey(self, session, scopes, count_of_accounts):
        data = {
            "scopes": scopes,
            "accounts": get_accounts(session, count=count_of_accounts)
        }
        response = requests.post(f'{trading_url}/api/auth/apikeys/new',
                               headers={'X-Auth-Nonce': session['nonce']},
                               cookies=session['cookies'], json=data)
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    #APIKEYS
    # TODO need to delete all api keys on terdown for apikey test
    def test_post_get_apikeys(self, session, apikey):
        response = requests.get(f'{trading_url}/api/auth/apikeys', headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_delete_apikey(self, session, apikey):
        data = {
            "apiKey": apikey['apiKey']
        }
        response = requests.delete(f'{trading_url}/api/auth/apikeys',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'], json=data)
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # 2FA
    def test_get_2fa_info(self, session, account):
        response = requests.get(f'{trading_url}/api/auth/account/{account}/2fa/info',
                              headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_2fa_generate(self, session, account):
        response = requests.post(f'{trading_url}/api/auth/account/{account}/2fa/generate',
                               headers={'X-Auth-Nonce': session['nonce']},
                               cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.skip(reason='too long')
    @pytest.mark.parametrize('generate2fa', [i for i in accounts if 'session_changing' in i['scopes']], indirect=True)
    @pytest.mark.parametrize('auth_enabled, enabled', [(True, False), (False, True), (True, True)])# False False is 2fa disabling
    def test_post_2fa_set(self, generate2fa, auth_enabled, enabled):
        session, otp_secret = generate2fa
        totp = pyotp.TOTP(otp_secret)
        logging.info(totp.now())
        data = {
            "password": session['login_data']['password'],
            "passcode": totp.now(),
            "authEnabled": auth_enabled,
            "enabled": enabled
        }
        response = requests.post(f'{trading_url}/api/auth/account/{get_accounts(session)[0]}/2fa/set',
                               headers={'X-Auth-Nonce': session['nonce']}, json=data,
                               cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

# OAUTH2

# TODO Update oauth section
@pytest.mark.skip(reason='no parametrize, no clients')
def test_get_oauth2_auth(self, session):
    response = requests.get(
        f"{trading_url}/api/auth/oauth2/auth?",
        address=trading_url,
        headers={'X-Auth-Nonce': session['nonce']},
        cookies=session['cookies'],
        allow_redirects=False)
    logging.info(response.headers)
    logging.info(response.text)
    assert response.status_code == 300


@pytest.mark.skip(reason='no parametrize, no clients')
def test_get_oauth2_info(self, session):
    response = requests.get(f"{trading_url}/api/auth/oauth2/info/.code.", address=trading_url,
                          headers={'X-Auth-Nonce': session['nonce']},
                          cookies=session['cookies'],
                          allow_redirects=False)
    logging.info(response.headers)
    logging.info(response.text)
    assert response.status_code == 200


@pytest.mark.skip(reason='no parametrize, no clients')
def test_get_oauth2_allow(self, session):
    response = requests.post(f"{trading_url}/api/auth/oauth2/allow/.code.",
                           address=trading_url, json={},
                           headers={'X-Auth-Nonce': session['nonce']},
                           cookies=session['cookies'],
                           allow_redirects=False)
    logging.info(response.headers)
    logging.info(response.text)
    assert response.status_code == 200


@pytest.mark.skip(reason='no parametrize, no clients')
def test_get_oauth2_token(self):
    data = {
        "grant_type": "authorization_code",
        "code": "",
        "client_id": "",
        "redirect_uri": "",
        "code_verifier": ""
    }
    response = requests.post(f"{trading_url}/api/auth/oauth2/token", address=trading_url,
                           json=data
                           )
    logging.info(response.headers)
    logging.info(response.text)
    assert response.status_code == 200
