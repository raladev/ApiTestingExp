class storage(dict):
    def __init__(self, dictionary):
        super.__init__()
        for k,v in dictionary:
            setattr(self, k, v)


def get_accounts(session, kind="all", count=100):
        a = []
        if kind in ["Spot", "Margin"]:
            a = [i['id'] for i in session['accounts']if kind == i['kind']]
        else:
            a = [i['id'] for i in session['accounts']]
        return a[:count]

