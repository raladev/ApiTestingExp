from tests.conftest import logging, trading_url
from utils import get_accounts
import requests
import pytest

# TODO Update after kyc passing
class TestCardPayPositive:

    def test_get_active_payments(self, session):
       response = requests.get(f'{trading_url}/api/payment/active-payments', headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       assert response.status_code == 200

    @pytest.mark.parametrize("base_amount", ["0.00400000"])
    def test_post_create_payment(self, session, payment_ratio, base_amount, cancel_payment):

       data = {"quoteAmount": str(round(float(base_amount)*float(payment_ratio), 2)),
               "quoteCurrency": "EUR",
               "baseAmount": base_amount,
               "baseCurrency": "BTC",
               "language": "ru",
               "ratio": payment_ratio,
               "account": get_accounts(session, kind='Spot')}
       response = requests.post(f'{trading_url}/api/payment/create',  headers={'X-Auth-Nonce': session['nonce']},
                             json=data, cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       assert response.status_code == 200

    def test_post_cancel(self, session):
        response = requests.post(f'{trading_url}/api/payment/cancel/0',
                               headers={'X-Auth-Nonce': session['nonce']},
                               cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_set_inective(self, session):
       response = requests.post(f'{trading_url}/api/payment/set-inactive/243941', headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       assert response.status_code == 200