from src.core.model import BaseModel
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.storehouse import Storehouse
from src.utils.validator import Validator


class StorehouseTurnover(BaseModel):
    __storehouse: Storehouse = None
    __turnover: int = None
    __nomenclature: Nomenclature = None
    __range: Range = None

    def local_eq(self, other: 'StorehouseTurnover'):
        return self.__turnover == other.__turnover and self.__storehouse == other.storehouse

    @classmethod
    def from_dict(cls, data: dict):
        Validator.check_fields(data=data, model=cls)
        obj = cls()
        obj.storehouse = data["storehouse"]
        obj.turnover = data["turnover"]
        obj.nomenclature = data["nomenclature"]
        obj.range = data["range"]
        obj.uuid = data['uuid']
        return obj

    @property
    def storehouse(self):
        return self.__storehouse

    @storehouse.setter
    def storehouse(self, new_storehouse: Storehouse):
        Validator.validate(new_storehouse, type_=Storehouse)
        self.__storehouse = new_storehouse

    @property
    def turnover(self):
        return self.__turnover

    @turnover.setter
    def turnover(self, new_turnover: int):
        Validator.validate(new_turnover, type_=int)
        self.__turnover = new_turnover

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, new_nomenclature):
        Validator.validate(new_nomenclature, type_=Nomenclature)
        self.__nomenclature = new_nomenclature

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, new_range):
        Validator.validate(new_range, type_=Range)
        self.__range = new_range

    @staticmethod
    def create(storehouse: Storehouse, turnover: int, nomenclature: Nomenclature, range: Range) -> 'StorehouseTurnover':
        Validator.validate(storehouse, type_=Storehouse)
        Validator.validate(turnover, type_=int)
        Validator.validate(nomenclature, type_=Nomenclature)
        Validator.validate(range, type_=Range)

        item = StorehouseTurnover()
        item.storehouse = storehouse
        item.turnover = turnover
        item.nomenclature = nomenclature
        item.range = range
        return item

    def __str__(self):
        return (f"StorehouseTurnover(storehouse={self.storehouse}, "
                f"turnover={self.turnover}, "
                f"nomenclature={self.nomenclature}, "
                f"range={self.range})")