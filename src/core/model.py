import uuid
from abc import ABC, abstractmethod

from src.utils.validator import Validator


class BaseModel(ABC):
    def __init__(self):
        self.__uuid = uuid.uuid4()

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, new_uui):
        Validator.validate(new_uui, str)
        self.__uuid = new_uui

    @abstractmethod
    def local_eq(self, other):
        pass

    def __eq__(self, other):
        return self.uuid == other.uuid or self.local_eq(other)
