class MyClass:
    def __new__(cls, *args, **kwargs):
        print("Creating a new instance of MyClass")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        print("Initializing the new instance of MyClass")

my_object = MyClass()
