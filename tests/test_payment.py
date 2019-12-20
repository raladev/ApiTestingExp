from tests.conftest import logging, trading_url
from src.client import client
import pytest


class TestCardpayPositive():

    def test_get_active_payments(self, session):
       response = client.get('/api/payment/active-payments', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

    def test_post_create_payment(self, session):
       data = {"quoteAmount":"25.72",
               "quoteCurrency":"EUR",
               "baseAmount":"0.00400000",
               "baseCurrency":"BTC",
               "language":"ru",
               "ratio":"6427.52",
               "account":8263441}
       response = client.post('/api/payment/create', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             json=data, cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

    def test_post_cancel(self, session):
        response = client.post('/api/payment/cancel/243941', address=trading_url,
                               headers={'X-Auth-Nonce': session['nonce']},
                               cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        response.assert_2xx()

    def test_post_set_inective(self, session):
       response = client.post('/api/payment/set-inactive/243941', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()