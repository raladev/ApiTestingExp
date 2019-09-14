import pytest
import logging
import json

base_url = 'https://trading.xena.exchange/'
logging.basicConfig(level=logging.INFO)

with open("../accounts.json", "r") as read_file:
    data = json.load(read_file)
    accounts = [i for i in data['accounts']]


def setup(request):
    logging.info('Start')

    def teardown():
        logging.info('End')
    request.addfinalizer(teardown)


class BaseTest(object):
    pass
