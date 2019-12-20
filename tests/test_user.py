from tests.conftest import logging, trading_url
from src.client import client
from utils import get_accounts, get_apikeys,generate_2fa_secret
import pyotp
import pytest


class TestUserPositive():
    #TODO Create account fixture
    @pytest.mark.parametrize("currency",["BTC",""])
    def test_post_create_margin(self, session, currency):
        data = {"currency":currency}
        response = client.post(path='api/user/create/margin', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                               json=data,cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    #NOTIFICATION
    def test_get_notification_settings(self, session):
        response = client.get(path='api/user/notification-settings', address=trading_url,
                                   headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    @pytest.mark.parametrize("settings",[ {"email": {"news":True}},
                                          {"email": {"news": True, "useForDeleveraging": False,}},
                                          {"email": {"news": False, "useForDeleveraging": True, "deposits": True}},
                                          {}
                                          ])

    def test_post_notification_settings(self, session, settings):
        response = client.post(path='api/user/notification-settings', address=trading_url,
                                   headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'], json=settings)
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    #DACCS
    def test_get_open_channels(self, session):
        response = client.get(path='api/user/daccs/open-channels', address=trading_url,
                              headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

    def test_get_channels_history(self, session):
        response = client.get(path='api/user/daccs/channels-history', address=trading_url,
                              headers={'X-Auth-Nonce': session['nonce']},
                              cookies=session['cookies'])
        logging.info(response.status_code)
        logging.info(response.text)
        response.assert_2xx()

