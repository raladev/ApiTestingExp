from tests.conftest import logging, base_url
import requests


class TestPagesPositive:

        def test_get_landing(self):
                response = requests.get(base_url)
                logging.info(response.text)
                assert response.status_code == 200
