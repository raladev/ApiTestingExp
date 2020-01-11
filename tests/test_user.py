from tests.conftest import logging, trading_url
import pytest
import requests


class TestUserPositive:

    # TODO Create account fixture
    @pytest.mark.skip(reason='no create account fixture')
    @pytest.mark.parametrize("currency", ["BTC", ""])
    def test_post_create_margin(self, session, currency):
        data = {"currency": currency}
        response = requests.post(f'{trading_url}/api/user/create/margin', headers={'X-Auth-Nonce': session['nonce']},
                               json=data, cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # NOTIFICATION
    def test_get_notification_settings(self, session):
        response = requests.get(f'{trading_url}/api/user/notification-settings',
                                   headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.parametrize("settings",[ {"email": {"news": True}},
                                          {"email": {"news": True, "useForDeleveraging": False}},
                                          {"email": {"news": False, "useForDeleveraging": True, "deposits": True}},
                                          {}
                                          ])
    def test_post_notification_settings(self, session, settings):
        response = requests.post(f'{trading_url}/api/user/notification-settings',
                                   headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'], json=settings)
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    # DACCS
    def test_get_open_channels(self, session):
        response = requests.get(f'{trading_url}/api/user/daccs/open-channels',
                              headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_channels_history(self, session):
        response = requests.get(f'{trading_url}/api/user/daccs/channels-history',
                              headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

