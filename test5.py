class A(object):
    def __init__(self):
        self.B = self.B()

    def get_B(self):
        return self.B.show()

    class B(object):
        def show(self):
            print("test !!!")


A().get_B()
