from tests.conftest import logging
from cfg import trading_url
import pytest
import requests


class TestProfilePositive:

    def test_get_profile_balances(self, session):
        response = requests.get(f'{trading_url}/api/profile/balances', headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_profile_accounts(self, session):
        response = requests.get(f'{trading_url}/api/profile/accounts', headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_profile_info(self, session):
        response = requests.get(f'{trading_url}/api/profile/info', headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_profile_settings(self, session):
        response = requests.get(f'{trading_url}/api/profile/settings', headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.parametrize('lang', ('RU', 'EN'))
    def test_post_profile_settings(self, session, lang):
        data = {
            'lang': lang
        }
        response = requests.post(f'{trading_url}/api/profile/settings', headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'], json=data)
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_affiliate_enroll(self, session):
        response = requests.post(f'{trading_url}/api/profile/affiliate/enroll',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_create_link(self, session):
        response = requests.post(f'{trading_url}/api/profile/affiliate/create_link',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_affiliate_links(self, session):
        response = requests.get(f'{trading_url}/api/profile/affiliate/links',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_affiliate_referrals(self, session):
        response = requests.get(f'{trading_url}/api/profile/affiliate/referrals',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_profile_cards(self, session):
        response = requests.get(f'{trading_url}/api/profile/cards', headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200
