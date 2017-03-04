class Infinity(object):
    def __init__(self):
        return
    def __eq__(self, other):
        return False
    def __gt__(self, other):
        return True
    def __ge__(self, other):
        return True
    def __le__(self, other):
        return False
    def __lt__(self, other):
        return False
