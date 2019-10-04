from tests.conftest import *
from src.client import client

def test_get_landing():
        response = client.get(address=base_url)
        response.assert_2xx()
