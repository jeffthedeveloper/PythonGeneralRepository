def setter(name):
    def inner(func):
        def wrapper(self, value):
            setattr(self, name, value)
            func(self, value)
        return wrapper
    return inner
