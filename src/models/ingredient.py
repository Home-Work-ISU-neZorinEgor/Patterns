from src.core.model import BaseModel
from src.models.nomenclature import Nomenclature
from src.utils.validator import Validator


class Ingredient(BaseModel):
    def local_eq(self, other):
        pass

    def __init__(self, nomenclature: Nomenclature, quantity: float | int):
        super().__init__()
        Validator.validate(nomenclature, type_=Nomenclature)
        Validator.validate(quantity, type_=int | float)
        self.__nomenclature = nomenclature
        self.__quantity = quantity

    @property
    def nomenclature(self):
        return self.__nomenclature

    @property
    def quantity(self):
        return self.__quantity

    def __str__(self):
        return f"{self.nomenclature} - {self.quantity}"
