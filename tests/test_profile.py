from tests.conftest import *
from src.client import client

@pytest.mark.parametrize("auth_data", accounts, ids=[i['desc'] for i in accounts], indirect=True)
class TestProfile(BaseTest):

        def test_get_profile_balances(self, auth_data):
                response = client.get('/api/profile/balances', address=trading_url, headers=pytest.session['X-Auth-Nonce'],
                                      cookies=pytest.session['sid'])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_get_profile_accounts(self, auth_data):
                response = client.get('/api/profile/accounts', address=trading_url, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_get_profile_info(self, auth_data):
                response = client.get('/api/profile/info', address=trading_url, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_get_profile_settings(self, auth_data):
                response = client.get('/api/profile/settings', address=trading_url, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        @pytest.mark.parametrize('lang',('ru', 'en', '', ';..'))
        def test_post_profile_settings(self, auth_data, lang):
                data = {
                        'lang': lang
                }
                response = client.post('/api/profile/settings', address=trading_url, json=data, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_post_affiliate_enroll(self, auth_data):
                response = client.post('/api/profile/affiliate/enroll', address=trading_url, headers=auth_data[0],
                                       cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_post_create_link(self, auth_data):
                response = client.post('/api/profile/affiliate/create_link', address=trading_url, headers=auth_data[0],
                                       cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_get_affiliate_links(self, auth_data):
                response = client.get('/api/profile/affiliate/links', address=trading_url, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_get_affiliate_referrals(self, auth_data):
                response = client.get('/api/profile/affiliate/referrals', address=trading_url, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()

        def test_get_profile_cards(self, auth_data):
                response = client.get('/api/profile/cards', address=trading_url, headers=auth_data[0],
                                      cookies=auth_data[1])
                logging.info(response.headers)
                logging.info(response.text)
                response.assert_2xx()