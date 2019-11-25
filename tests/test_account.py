from tests.conftest import logging, trading_url
from src.client import client
import pytest


class TestAccountPositive():

    def test_get_account(self, session, account):
       response = client.get('/api/account/'+account, address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

    def test_get_balances(self, session, account):
       response = client.get('/api/account/' + account + '/balances', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

    def test_get_deposit_address(self, session, account, account_currency):
        response = client.get('/api/account/' + account + '/deposit/' + account_currency + '/address', address=trading_url,
                              headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        response.assert_2xx()

    @pytest.mark.parametrize('name',['\r\n',
                                     'null',
                                     '*[]its#20$символов!/',
                                     '\u200b',
                                     '$;--한글']
                             )
    def test_post_info(self, session, account, name):
       data = {
        'name': name
       }
       response = client.post('/api/account/' + account + '/info', address=trading_url, json=data, headers={'X-Auth-Nonce': session['nonce']},
                             cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       response.assert_2xx()

class TestAccountNegative():

    def test_get_account(self, session, negative_account):
       logging.info(str(session) + negative_account)
       response = client.get('/api/account/'+negative_account, address=trading_url,
                             headers={'X-Auth-Nonce': session['nonce']}, cookies=session['cookies'])
       logging.info(response.headers)
       logging.info(response.text)
       logging.info(response.status_code)
       # response.assert_2xx()