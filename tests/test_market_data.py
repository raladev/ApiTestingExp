from tests.conftest import *
from src.client import client
import logging

@pytest.mark.parametrize("currency", ["XBTUSD", "ETH/USDT", "BTC/USDT"])
def test_get_candles(currency):
    response = client.get(address=trading_url, path='/api/market-data/candles/' + currency + '/1h')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

@pytest.mark.parametrize("currency", ["XBTUSD", "ETH/USDT", "BTC/USDT"])
def test_get_dom(currency):
    response = client.get(address=trading_url, path='/api/market-data/dom/' + currency)
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

#trendpower, compare with perpetuals
def test_get_initials_candles():
    response = client.get(address=trading_url, path='/api/market-data/initial/candles')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_perpetuals():
    response = client.get(address=trading_url, path='/api/market-data/perpetuals')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

#USDETH no trendpower
def test_get_investments():
    response = client.get(address=trading_url, path='/api/market-data/investments')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

# why indexes is in market watch
def test_get_market_watch():
    response = client.get(address=trading_url, path='/api/market-data/market-watch')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

# what is https://trading.xena.exchange/api/market-data/indexes/.BTC3_TWAP/BTC/USDT/1h