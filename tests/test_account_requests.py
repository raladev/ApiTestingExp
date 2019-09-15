from src.client import client
from tests.conftest import *

class TestAccountRequests(BaseTest):

    @pytest.mark.parametrize("account", accounts)
    def test_post_login(self, account):
        response = client.post(path='/api/auth/login', address=trading_url, json=account)
        response.assert_2xx()

    @pytest.mark.skip(reason='Because of GoogleCapcha')
    def test_post_registration(self):
        data = {}
        response = client.post('/api/register/new', address=trading_url, json=data)
        response.assert_2xx()