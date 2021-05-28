# https://qiita.com/t2y/items/3ecdc2643426a345d75a

from abc import ABCMeta, abstractmethod
# abc --- Abstract Base Class

class ICarElementVisitor(metaclass=ABCMeta):
    """
    Interfaceのようなものin Python
    """
    @abstractmethod
    def visit_wheel(self, wheel): pass

    @abstractmethod
    def visit_engine(self, engine): pass

    @abstractmethod
    def visit_body(self, body): pass

    @abstractmethod
    def visit_car(self, car): pass


class ICarElement(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass


class Wheel(ICarElement):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit_wheel(self)


class Engine(ICarElement):
    def accept(self, visitor):
        visitor.visit_engine(self)


class Body(ICarElement):
    def accept(self, visitor):
        visitor.visit_body(self)


class Car(ICarElement):
    def __init__(self):
        self.elements = [
            Wheel('front left'),
            Wheel('front right'),
            Wheel('back left'),
            Wheel('back right'),
            Body(),
            Engine()
        ]

    def accept(self, visitor):
        for elem in self.elements:
            elem.accept(visitor)
        visitor.visit_car(self)


class PrintVisitor(ICarElementVisitor):
    def visit_wheel(self, wheel):
        print("Visiting {} wheel".format(wheel.name))

    def visit_engine(self, wheel):
        print("Visiting engine")

    def visit_body(self, wheel):
        print("Visiting body")

    def visit_car(self, wheel):
        print("Visiting car")


class DoVisitor(ICarElementVisitor):
    def visit_wheel(self, wheel):
        print('Kicking my {} wheel'.format(wheel.name))

    def visit_engine(self, wheel):
        print("Starting my engine")

    def visit_body(self, wheel):
        print("Moving my body")

    def visit_car(self, wheel):
        print("Driving my car")


def main():
    print("Visitor Pattern in Python demo")
    car = Car()
    car.accept(PrintVisitor())
    print('-' * 32)
    car.accept(DoVisitor())


main()
