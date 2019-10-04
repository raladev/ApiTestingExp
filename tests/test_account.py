from tests.conftest import *
from src.client import client

@pytest.mark.parametrize("auth_data", accounts, ids=[i['desc'] for i in accounts], indirect=['accounts'])
class TestAccount(BaseTest):

    @pytest.mark.parametrize("account")
    def test_get_account(self, account, auth_data):
        response = client.get('/api/account/'+account, address=trading_url, headers=auth_data[0],
                              cookies=auth_data[1])
        logging.info(response.headers)
        logging.info(response.text)
        response.assert_2xx()