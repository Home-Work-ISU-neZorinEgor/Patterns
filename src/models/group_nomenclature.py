from src.core.model import BaseModel
from src.utils.validator import Validator


class GroupNomenclature(BaseModel):
    __name = ""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    def local_eq(self, other):
        return self.__name == other.__name

    @staticmethod
    def create(name="Сырье"):
        item = GroupNomenclature()
        item.name = name  # Используем сеттер
        return item

    def __str__(self):
        return f"{self.__name}, uuid: {self.uuid}"
