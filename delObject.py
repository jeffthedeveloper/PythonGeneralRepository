class MyClass:
    def __init__(self, filename):
        self.file = open(filename, "w")

    def __del__(self):
        if self.file is not None:
            self.file.close()

my_object = MyClass("my_file.txt")

# The file is now open

del my_object

# The file is now closed
