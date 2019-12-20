from tests.conftest import logging, trading_url
from src.client import client
from utils import get_accounts, get_apikeys,generate_2fa_secret
import pyotp
import pytest


class TestAuthPositive():

        # AUTH
        # @pytest.mark.parametrize("login_data", accounts, ids=[i['desc'] for i in accounts])
        #def test_post_login(self, login_data):
        #         response = client.post(path='/api/auth/login', address=trading_url, json=account['login_data'])
        #         logging.info(response.status_code)
        #         logging.info(response.text)
     #           response.assert_2xx()

        def test_post_renew(self, session):
            response = client.post(path='/api/auth/renew', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
            logging.info(response.status_code)
            logging.info(response.text)
            response.assert_2xx()

        def test_post_logout(self, session):
            response = client.post(path='/api/auth/logout', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'], json={})
            logging.info(response.status_code)
            logging.info(response.text)
            response.assert_2xx()

        # APIKEYS
        def test_post_get_apikeys(self, session):
            response = client.get(path='/api/auth/apikeys', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                           cookies=session['cookies'])
            logging.info(response.status_code)
            logging.info(response.text)
            response.assert_2xx()

        @pytest.mark.parametrize("scopes, cnt",[(["trading","transfers", "daccs"],1),
                                                (["readOnlyTrading", "readOnlyBalanceOperations"],3),
                                                (["daccs"],6)])
        def test_post_post_new_apikey(self, session, scopes, cnt):
            data = {
                "scopes": scopes,
                "accounts":get_accounts(session, count=cnt)
            }

            response = client.post(path='/api/auth/apikeys/new', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                           cookies=session['cookies'], json=data)
            logging.info(response.status_code)
            logging.info(response.text)
            response.assert_2xx()

        def test_post_post_delete_apikey(self, session):
            data = {
                "apiKey": get_apikeys(session, count=1)[0]['apiKey']
            }
            response = client.delete(path='/api/auth/apikeys', address=trading_url,
                           headers={'X-Auth-Nonce': session['nonce']},
                           cookies=session['cookies'], json=data)
            logging.info(response.status_code)
            logging.info(response.text)
            response.assert_2xx()

        #2FA
        def test_get_2fa_info(self, session, account):
            response = client.get('/api/auth/account/' + account + '/2fa/info', address=trading_url,
                                  headers={'X-Auth-Nonce': session['nonce']},
                                  cookies=session['cookies'])
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_2xx()

        def test_post_2fa_generate(self,session, account):
            response = client.post('/api/auth/account/' + account + '/2fa/generate', address=trading_url,
                                  headers={'X-Auth-Nonce': session['nonce']},
                                  cookies=session['cookies'])
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_2xx()

        def test_post_2fa_set(self,session):
            otp_secret = generate_2fa_secret(session)
            totp = pyotp.TOTP(otp_secret)
            data = {
                "password":session['login_data']['password'],
                "passcode":totp.now(),
                "authEnabled": False,
                "enabled": False
            }
            response = client.post('/api/auth/account/' + str(get_accounts(session)[0]) + '/2fa/set', address=trading_url,
                                  headers={'X-Auth-Nonce': session['nonce']}, json=data,
                                  cookies=session['cookies'])
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_2xx()

        #OAUTH2
        def test_get_oauth2_auth(self,session):
            response = client.get("/api/auth/oauth2/auth?response_type=code&client_id=xenapro&redirect_uri=http://localhost:49152/&scope=trading&state=29c35bff639446bf98020f1d748024e6&code_challenge=dqM3GCD3NfGXtDf9Z1sJZ3bYDPdUFx7ZuBnoHu_RnE8=&code_challenge_method=S256", address=trading_url,
                                  headers={'X-Auth-Nonce': session['nonce']},
                                  cookies=session['cookies'],
                                  allow_redirects=False)
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_3xx()

        @pytest.skip(reason='no parametrize')
        def test_get_oauth2_info(self,session):
            response = client.get("/api/auth/oauth2/info/W5trqKXDaRBULRZNvh65OHqG6Lp_2d4FiIfKul0byPY", address=trading_url,
                                  headers={'X-Auth-Nonce': session['nonce']},
                                  cookies=session['cookies'],
                                  allow_redirects=False)
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_2xx()

        @pytest.skip(reason='no parametrize')
        def test_get_oauth2_allow(self,session):
            response = client.post("/api/auth/oauth2/allow/YHiV1xd4M7jPYhGNA3Uhxz7fT2hAZR_wGzAShKVeUVI", address=trading_url, json={},
                                  headers={'X-Auth-Nonce': session['nonce']},
                                  cookies=session['cookies'],
                                  allow_redirects=False)
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_2xx()

        @pytest.skip(reason='no parametrize')
        def test_get_oauth2_token(self):
            data = {
                    "grant_type":"authorization_code",
                    "code":"h3-d2Rt-rSE0xOVD-q0KZ_mgVcHXUZ_bd4QkfBtVb8brNWX30Dt92sLHVN5QM4dlsZ6OrAIQyYdnxQuzq0tlxA",
                    "client_id":"xenapro",
                    "redirect_uri":"http://localhost:49152/",
                    "code_verifier":"ca8d5a37981b41a49338c4bf7de3c7e5"
                    }
            response = client.post("/api/auth/oauth2/token", address=trading_url,
                                   json=data
                                  )
            logging.info(response.headers)
            logging.info(response.text)
            response.assert_2xx()

