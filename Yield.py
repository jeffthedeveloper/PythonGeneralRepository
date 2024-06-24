def geradores():
    for i in range(10):
        yield i

it = geradores()
print(next(it))
print(next(it))
print(next(it))
