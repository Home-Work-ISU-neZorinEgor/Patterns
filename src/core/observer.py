from abc import ABC, abstractmethod
from enum import Enum

from src.core.model import BaseModel
from src.utils.validator import Validator


class EventType(Enum):
    DELETE_NOMENCLATURE = 0
    UPDATE_NOMENCLATURE = 1

    ON_SAVE_DUMP = 2


class Observer(ABC):
    @abstractmethod
    def check_statement(self, event_type: EventType, entity: BaseModel):
        raise NotImplementedError("Метод check_statement() должен быть реализован.")


class Subject:
    def __init__(self):
        self.__validator = Validator()
        self.__observers: list[Observer] = []
        self.__validator.validate(self.__observers, type_=list[Observer])

    def attach(self, observer: Observer):
        self.__validator.validate(observer, Observer)
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self, event_type: EventType, entity: BaseModel | None):
        for observer in self.__observers:
            observer.check_statement(event_type=event_type, entity=entity)

