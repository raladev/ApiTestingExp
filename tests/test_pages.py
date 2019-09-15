from src.client import client
from tests.conftest import *


class TestPages(BaseTest):

    def test_get_landing(self):
        response = client.get(address=base_url)
        response.assert_2xx()
