import pytest
import logging
import json

ws_url = ''
trading_url = 'https://trading.xena.exchange/'
base_url = 'https://xena.exchange/'

logging.basicConfig(level=logging.INFO)

with open("../accounts.json", "r") as read_file:
    data = json.load(read_file)
    accounts = [i for i in data['accounts']]


@pytest.fixture(scope='session', autouse=True)
def init_tests():
    logging.info('Start')

    yield

    logging.info('End')


class BaseTest(object):
    pass
