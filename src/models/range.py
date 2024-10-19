from src.core.model import BaseModel
from src.utils.validator import Validator


class Range(BaseModel):
    __name = None
    __conversion_factor = None
    __base_unit = None

    def local_eq(self, other):
        # Сравниваем по имени или по коду, если он есть
        if isinstance(other, Range):
            return self.__name == other.__name or self.__code == other.__code
        return False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        Validator.validate(new_name, type_=str)
        self.__name = new_name

    @property
    def base_unit(self):
        return self.__base_unit

    @base_unit.setter
    def base_unit(self, new_unit):
        Validator.validate(new_unit, type_=Range | None)
        self.__base_unit = new_unit

    @property
    def conversion_factor(self):
        return self.__conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, new_factor):
        Validator.validate(new_factor, type_=int)
        self.__conversion_factor = new_factor

    def convert_to_base(self, value):
        return value * self.__conversion_factor

    def convert_from_base(self, value):
        return value / self.__conversion_factor

    def __str__(self):
        return f"uuid: {self.uuid}, name: {self.__name}, conversion_factor: {self.__conversion_factor}, base_unit: {self.__base_unit}"

    @staticmethod
    def create(name, conversion_factor, base_unit=None):
        item = Range()
        item.__name = name
        item.__conversion_factor = conversion_factor
        if base_unit is None:
            base = Range()
            base.__name = None
            base.__conversion_factor = None
            base.__base_unit = None
        else:
            item.__base_unit = base_unit
        return item
