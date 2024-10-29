import uuid
from abc import ABC, abstractmethod


from src.utils.validator import Validator


class BaseModel(ABC):
    __uuid: str = str(uuid.uuid4())

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, new_uuid):
        Validator.validate(new_uuid, str)
        self.__uuid = new_uuid

    @abstractmethod
    def local_eq(self, other):
        pass

    def __eq__(self, other):
        return self.uuid == other.uuid or self.local_eq(other)

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        obj = cls()
        if 'uuid' in data:
            obj.uuid = data['uuid']
        return obj
