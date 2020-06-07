class A:
    def fun(self):
        print('我是实例/对象方法，我是最普通和常见的类方法')


class Game:
    @staticmethod
    def meun():
        print("我是静态方法")


class Person:
    type = '人类'

    @classmethod
    def test(cls):
        print(cls.type)


class Goods:
    a = 2
    __discount = 1

    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def change_discount(cls, new_discount):
        cls.__discount = new_discount

    @property
    def finally_price(self):
        return self.price * self.__discount


if __name__ == '__main__':
    # A().fun()
    # Game.meun()
    # Person.test()

    banana = Goods('香蕉', 10)
    apple = Goods('苹果', 16)
    Goods.change_discount(0.8)
    print(banana.finally_price)
    print(apple.finally_price)

    Goods.change_discount(0.5)
    print(banana.finally_price)
    print(apple.finally_price)
