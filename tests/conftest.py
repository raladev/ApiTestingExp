import pytest
import logging
import json
import requests

ws_url = 'ws//:trading.xena.exchange/'
trading_url = 'https://trading.xena.exchange/'
base_url = 'https://xena.exchange/'

logging.basicConfig(level=logging.INFO)

with open("../accounts.json", "r") as read_file:
    data = json.load(read_file)
    accounts = [i for i in data['accounts']]
    print(accounts)

@pytest.fixture(scope='session', autouse=True)
def init_tests():
    logging.info('Start')

    yield

    logging.info('End')

@pytest.fixture(scope='class')
def auth_data(request):
    logging.info('\r\nStart auth_data fixture\r\n')
    response = requests.post(url=trading_url+'/api/auth/login', json=request.param)
    try:
        jresp = json.loads(response.text)
    except:
        logging.info('Incorrect response is ' + response.text)
    yield ({'X-Auth-Nonce': jresp['nonce']},{'sid': response.cookies['sid'],},1)




class BaseTest:
    pass