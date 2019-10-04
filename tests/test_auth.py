from tests.conftest import *
from src.client import client


@pytest.mark.parametrize("account", accounts, ids=[i['desc'] for i in accounts])
def test_post_login(account):
    response = client.post(path='/api/auth/login', address=trading_url, json=account)
    logging.info(response.status_code)
    logging.info(response.text)
    response.assert_2xx()