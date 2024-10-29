from src.core.model import BaseModel
from src.utils.validator import Validator


class Storehouse(BaseModel):
    __address: str = ""

    def local_eq(self, other: 'Storehouse'):
        return self.address == other.address

    @classmethod
    def from_dict(cls, data: dict):
        Validator.check_fields(data=data, model=cls)
        Validator.validate(data, type_=dict)  # Проверяем, что передан словарь
        Validator.validate(data.get('address'), str)  # Проверяем, что адрес является строкой

        storehouse = cls()
        storehouse.address = data['address']
        storehouse.uuid = data.get('uuid', storehouse.uuid)  # Если в данных есть UUID, задаем его

        return storehouse

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, new_address):
        Validator.validate(new_address, str)
        self.__address = new_address

    @staticmethod
    def create(address: str):
        Validator.validate(address, type_=str)
        storehouse = Storehouse()
        storehouse.address = address
        return storehouse

    def __str__(self):
        return f"Storehouse(address={self.address})"
