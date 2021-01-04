"""
Illustrates the difference between type.__init__ and __new__
"""


class Yoyo:
    def __new__(cls, *args, **kwargs):
        print("new called")
        return super().__new__(cls)

    def __init__(self):
        pass


# will call new 10 times
[Yoyo() for _ in range(10)]


class _MyMeta(type):
    def __init__(cls, name, base, attrs):
        print("meta new called")
        super().__init__(name, base, attrs)


class Yoyo2(metaclass=_MyMeta):
    def __init__(self):
        pass


# will call new only once!!
[Yoyo2() for _ in range(10)]
