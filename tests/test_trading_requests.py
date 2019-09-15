from src.client import client
from tests.conftest import *
import logging


class TestTradingRequests(BaseTest):

    def test_get_commissions(self):
        response = client.get(address=trading_url, path='/api/common/commissions')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    def test_get_features(self):
        response = client.get(address=trading_url, path='/api/common/features')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    def test_get_instruments(self):
        response = client.get(address=trading_url, path='/api/common/instruments')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    def test_get_currencies(self):
        response = client.get(address=trading_url, path='/api/common/currencies')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    @pytest.mark.parametrize("currency", ["XBTUSD", "ETH/USDT", "BTC/USDT"])
    def test_get_market_data(self, currency):
        response = client.get(address=trading_url, path='/api/market-data/candles/'+currency+'/1h')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    def test_get_perpetuals(self):
        response = client.get(address=trading_url, path='/api/market-data/perpetuals')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    def test_get_investments(self):
        response = client.get(address=trading_url, path='/api/market-data/investments')
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()
