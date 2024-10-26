from src.core.model import BaseModel
from src.models.nomenclature import Nomenclature
from src.utils.validator import Validator


class Ingredient(BaseModel):
    __nomenclature: Nomenclature
    __quantity: int

    def local_eq(self, other: 'Ingredient'):
        return self.nomenclature == other.nomenclature

    @classmethod
    def from_dict(cls, data: dict):
        Validator.check_fields(data=data, model=cls)
        obj = cls()
        obj.nomenclature = Nomenclature.from_dict(data['nomenclature'])
        obj.quantity = data['quantity']
        obj.uuid = data['uuid']
        return obj

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, new_nomenclature):
        Validator.validate(new_nomenclature, type_=Nomenclature)
        self.__nomenclature = new_nomenclature

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity):
        Validator.validate(new_quantity, type_=int | float)
        self.__quantity = new_quantity

    @staticmethod
    def create(nomenclature: Nomenclature, quantity: float | int):
        Validator.validate(nomenclature, type_=Nomenclature)
        Validator.validate(quantity, type_=int | float)
        item = Ingredient()
        item.nomenclature = nomenclature
        item.quantity = quantity
        return item

    def __str__(self):
        return f"{self.nomenclature} - {self.quantity}"
