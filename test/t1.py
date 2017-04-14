
class Parent():
    name = "parent"

    def met(self):
        print self.name


class Son(Parent):
    name = "son"


if __name__ == '__main__':
    son = Son()
    son.met()