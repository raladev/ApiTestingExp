from tests.conftest import logging, trading_url
from src.client import client
import pytest


class TestKYCPositive():

    def test_get_kyc_status(self, session):
       response = client.get('/api/kyc/status', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

    def test_post_kyc_application(self, session):
       response = client.post('/api/kyc/application', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             json={},cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

    def test_post_kyc_telegram(self, session):
        response = client.post('/api/kyc/telegram-passport', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                               cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        response.assert_2xx()