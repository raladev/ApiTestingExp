from tests.conftest import logging, trading_url
import requests
import pytest


class TestMarketDataPositive:

    @pytest.mark.parametrize("currency", ["XBTUSD", "ETH/USDT", "BTC/USDT"])
    def test_get_candles(self, currency):
        response = requests.get(f'{trading_url}/api/market-data/candles/{currency}/1h')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.parametrize("currency", ["XBTUSD", "ETH/USDT", "BTC/USDT"])
    def test_get_dom(self, currency):
        response = requests.get(f'{trading_url}/api/market-data/dom/{currency}')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # trendpower, compare with perpetuals
    def test_get_initials_candles(self):
        response = requests.get(f'{trading_url}/api/market-data/initial/candles')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_perpetuals(self):
        response = requests.get(f'{trading_url}/api/market-data/perpetuals')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # USDETH no trendpower
    def test_get_investments(self):
        response = requests.get(f'{trading_url}/api/market-data/investments')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # why indexes is in market watch
    def test_get_market_watch(self):
        response = requests.get(f'{trading_url}/api/market-data/market-watch')
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # what is https://trading.xena.exchange/api/market-data/indexes/.BTC3_TWAP/BTC/USDT/1h
