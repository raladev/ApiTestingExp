from tests.conftest import BaseTest, logging
from src.client import client



class TestAccount():

    def test_get_account(self, session, neg_or_pos_account, expected_result):
       logging.info(session, neg_or_pos_account, expected_result)
       # response = client.get('/api/account/'+account, address=trading_url, headers={'X-Auth-Nonce': sessio['nonce']},
       #                      cookies=sessio['cookies'])
       # logging.info(response.headers)
       # logging.info(response.text)
       # response.assert_2xx()

