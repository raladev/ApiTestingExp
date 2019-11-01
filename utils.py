
class storage(dict):

    def __init__(self, dictionary):
        super.__init__()
        for k,v in dictionary:
            setattr(self, k, v)

