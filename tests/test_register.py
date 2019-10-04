from tests.conftest import *
from src.client import client

@pytest.mark.skip(reason='Because of GoogleCapcha')
def test_post_registration(self):
    data = {}
    response = client.post('/api/register/new', address=trading_url, json=data)
    response.assert_2xx()