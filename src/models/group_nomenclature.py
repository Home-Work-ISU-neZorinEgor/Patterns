from src.core.model import BaseModel
from src.utils.validator import Validator


class GroupNomenclature(BaseModel):
    __name: str = ""

    def local_eq(self, other):
        return self.__name == other.__name

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj.name = data['name']
        obj.uuid = data['uuid']
        return obj

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    @staticmethod
    def create(name="Сырье"):
        Validator.validate(name, type_=str)
        item = GroupNomenclature()
        item.name = name
        return item

    def __str__(self):
        return f"{self.__name}, uuid: {self.uuid}"
