from profile import profile


@profile
class Test():
    def __init__(self):
        pass

    def countdown(self, n):
        while n > 0:
            n -= 1


@profile
def foo():
    pass


@profile
class Bar():
    def __init__(self):
        pass


@profile
def countdown(n):
    while n > 0:
        n -= 1


foo()
Bar()
countdown(1000)

t = Test()
t.countdown(1000)
