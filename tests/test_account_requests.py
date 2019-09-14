from src.client import client
from tests.conftest import *
import logging


class TestAccountRequests(BaseTest):

    @pytest.mark.parametrize("account", accounts)
    def test_login(self, account):
        response = client.post('/api/auth/login', json=account)
        response.assert_2xx()
