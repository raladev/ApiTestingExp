from tests.conftest import logging, trading_url
import requests


class TestKYCPositive:

    def test_get_kyc_status(self, session):
        response = requests.get(f'{trading_url}/api/kyc/status', headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_kyc_application(self, session):
        response = requests.post(f'{trading_url}/api/kyc/application', headers={'X-Auth-Nonce': session['nonce']},
                                 json={}, cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_kyc_telegram(self, session):
        response = requests.post(f'{trading_url}/api/kyc/telegram-passport', headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200
