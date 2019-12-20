from tests.conftest import trading_url
from src.client import client
import ast

class storage(dict):

    def __init__(self, dictionary):
        super.__init__()
        for k,v in dictionary:
            setattr(self, k, v)

#Methods for current session
#TODO Session class of fixtures?
def get_accounts(session, kind="all", count=100):
        a = []
        if kind in ["Spot", "Margin"]:
            a = [i['id'] for i in session['accounts']if kind == i['kind']]
        else:
            a = [i['id'] for i in session['accounts']]
        return a[:count]

def get_apikeys(session, count=100):
    response = client.get(path='/api/auth/apikeys', address=trading_url, headers={'X-Auth-Nonce': session['nonce']},
                          cookies=session['cookies'])
    a = ast.literal_eval(response.text)
    return a

def generate_2fa_secret(session):
    response = client.post('/api/auth/account/' + str(get_accounts(session)[0]) + '/2fa/generate', address=trading_url,
                           headers={'X-Auth-Nonce': session['nonce']},
                           cookies=session['cookies'])
    a = ast.literal_eval(response.text)
    return a['key']

