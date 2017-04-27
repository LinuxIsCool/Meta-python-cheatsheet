"""
More concrete examples
"""

class Gimme5(object):
    def __new__(cls, *args, **kwargs):
        print('Gimme5.__new__', args, kwargs)
        return 5
    
    def __init__(self, whatever):
        raise RuntimeError('SHOULD NOT BE CALLED')

assert Gimme5('yo') is 5


class MonsterA(object):
    """
    Monstrous abuse of __new__:
    https://concentricsky.com/articles/detail/pythons-hidden-new
    """
    def __new__(cls, *args, **kwargs):
        return super(MonsterA,cls).__new__(MonsterB)

    def __init__(self):
        # init will NOT be called when __new__ returns an incompatible type
        self.name = "MonsterA"


class MonsterB(object):
    def __new__(cls, *args, **kwargs):
        return super(MonsterB,cls).__new__(MonsterA)

    def __init__(self):
        self.name = "MonsterB"


a = MonsterA()
b = MonsterB()
assert type(a) == MonsterB
assert type(b) == MonsterA
assert hasattr(a, 'name') is False
assert hasattr(b, 'name') is False