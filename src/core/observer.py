from abc import ABC, abstractmethod

from src.utils.validator import Validator


class Observer(ABC):
    @abstractmethod
    def update(self, message):
        raise NotImplementedError("Метод update() должен быть реализован.")


class Subject:
    def __init__(self):
        self.__validator = Validator()
        self.__observers: list[Observer] = []
        self.__validator.validate(self.__observers, list[Observer])

    def attach(self, observer: Observer):
        self.__validator.validate(observer, Observer)
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer):
        try:
            self.__observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message):
        for observer in self.__observers:
            observer.update(message)
