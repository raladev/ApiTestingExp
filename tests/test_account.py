from tests.conftest import logging
from cfg import trading_url
import pytest
import requests
from utils import get_accounts
import time


class TestAccountPositive:

    def test_get_account(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_balances(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/balances',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_deposit_address(self, session, account, account_currency):
        response = requests.get(f'{trading_url}/api/account/{account}/deposit/{account_currency}/address',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_post_renew_deposit_address(self, session, account, account_currency):
        response = requests.post(f'{trading_url}/api/account/{account}/deposit/{account_currency}/renew',
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_withdraw_limit(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/withdraw/limit',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_trusted_addresses(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/withdraw/trusted-addresses',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.skip(reason='skipped for prod')
    @pytest.mark.parametrize('kind_from, kind_to', [
        ("Spot", "Margin"),
        ("Margin", "Margin"),
        ("Margin", "Spot")
    ])
    def test_post_internal_transfer(self, session, kind_from, kind_to):
        from_account = get_accounts(session, kind=kind_from)[0]
        to_account = list(set(get_accounts(session, kind=kind_to)).symmetric_difference([from_account]))[0]
        data = {
                "id": str(time.time_ns()),
                "fromAccount": int(from_account),
                "toAccount": int(to_account),
                "amount": "0.00010000",
                "currency": "BTC"
                }
        response = requests.get(f'{trading_url}/api/account/{get_accounts(session)[0]}/internal-transfer',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_active_transactions(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/active-transactions',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_trade_history(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/trade-history',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_balance_history(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/balance-history',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    # TODO Need fixture only for margin account
    @pytest.mark.skip(reason='400 for spot account - correct behavior')
    def test_get_positions_history(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/positions-history',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_open_positions(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/open-positions',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies']
                                )
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.parametrize('position_accounting', ["Netting", "Hedging"])
    def test_post_info_accounting(self, session, account, position_accounting):
        data = {
            'positionAccounting': position_accounting
        }
        response = requests.post(f'{trading_url}/api/account/{account}/info', json=data,
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    @pytest.mark.parametrize('name', ['\r\n', 'null', '*[]its#20$символов!/', '\u200bu', '$;--한글'])
    def test_post_info_acc_name(self, session, account, name):
        data = {
            'name': name
        }
        response = requests.post(f'{trading_url}/api/account/{account}/info', json=data,
                                 headers={'X-Auth-Nonce': session['nonce']},
                                 cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200

    def test_get_upcoming_rebates(self, session, account):
        response = requests.get(f'{trading_url}/api/account/{account}/rebates/upcoming',
                                headers={'X-Auth-Nonce': session['nonce']},
                                cookies=session['cookies'])
        logging.info(response.headers)
        logging.info(response.text)
        assert response.status_code == 200


class TestAccountNegative:
    pass
