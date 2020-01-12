from tests.conftest import logging
from cfg import trading_url
import requests


class TestCommonPositive:

    def test_get_commissions(self):
        response = requests.get(f'{trading_url}/api/common/commissions')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_features(self):
        response = requests.get(f'{trading_url}/api/common/features')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_instruments(self):
        response = requests.get(f'{trading_url}/api/common/instruments')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_currencies(self):
        response = requests.get(f'{trading_url}/api/common/currencies')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_currency_ratios(self):
        response = requests.get(f'{trading_url}/api/common/currency-ratios')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # last trades
    def test_get_last_prices(self):
        response = requests.get(f'{trading_url}/api/common/last-prices')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_kyc(self):
        response = requests.get(f'{trading_url}/api/common/kyc')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_referral_levels(self):
        response = requests.get(f'{trading_url}/api/common/referral-levels')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_historical_currency_ratios(self):
        response = requests.get(f'{trading_url}/api/common/historical-currency-ratios')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_blocked_countries(self):
        response = requests.get(f'{trading_url}/api/common/blocked-countries')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_payment_ratio(self):
        response = requests.get(f'{trading_url}/api/common/payment/ratio')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_paysystems(self):
        response = requests.get(f'{trading_url}/api/common/paysystems')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_paysystem_countries(self):
        response = requests.get(f'{trading_url}/api/common/paysystem-countries')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_news(self):
        response = requests.get(f'{trading_url}/api/common/news')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_spec_margin_trading(self):
        response = requests.get(f'{trading_url}/api/common/platform-specification/margin-trading')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200
