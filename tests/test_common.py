from tests.conftest import *
from src.client import client
import logging

def test_get_commissions():
    response = client.get(address=trading_url, path='/api/common/commissions')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()


def test_get_features():
    response = client.get(address=trading_url, path='/api/common/features')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()


def test_get_instruments():
    response = client.get(address=trading_url, path='/api/common/instruments')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()


def test_get_currencies():
    response = client.get(address=trading_url, path='/api/common/currencies')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_currency_ratios():
    response = client.get(address=trading_url, path='/api/common/currency-ratios')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

# last trades
def test_get_last_prices():
    response = client.get(address=trading_url, path='/api/common/last-prices')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_kyc():
    response = client.get(address=trading_url, path='/api/common/kyc')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_referral_levels():
    response = client.get(address=trading_url, path='/api/common/referral-levels')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_historical_currency_ratios():
    response = client.get(address=trading_url, path='/api/common/historical-currency-ratios')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_blocked_countries():
    response = client.get(address=trading_url, path='/api/common/blocked-countries')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_payment_ratio():
    response = client.get(address=trading_url, path='/api/common/payment/ratio')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_paysystems():
    response = client.get(address=trading_url, path='/api/common/paysystems')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_paysystem_countries():
    response = client.get(address=trading_url, path='/api/common/paysystem-countries')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

def test_get_news():
    response = client.get(address=trading_url, path='/api/common/news')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()

# only liquidation level?
def test_spec_margin_trading():
    response = client.get(address=trading_url, path='/api/common/platform-specification/margin-trading')
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()
