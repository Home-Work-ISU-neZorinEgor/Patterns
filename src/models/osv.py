from src.core.model import BaseModel
from src.utils.validator import Validator


class OSV(BaseModel):
    __nomenclature_name: str = None
    __initial_balance: int = None
    __turnover: int = None
    __final_balance: int = None

    @property
    def nomenclature_name(self):
        return self.__nomenclature_name

    @nomenclature_name.setter
    def nomenclature_name(self, new_nomenclature_name: str):
        Validator.validate(new_nomenclature_name, type_=str)
        self.__nomenclature_name = new_nomenclature_name

    @property
    def initial_balance(self):
        return self.__initial_balance

    @initial_balance.setter
    def initial_balance(self, new_initial_balance: int):
        Validator.validate(new_initial_balance, type_=int)
        self.__initial_balance = new_initial_balance

    @property
    def turnover(self):
        return self.__turnover

    @turnover.setter
    def turnover(self, new_turnover: int):
        Validator.validate(new_turnover, type_=int)
        self.__turnover = new_turnover

    @property
    def final_balance(self):
        return self.__final_balance

    @final_balance.setter
    def final_balance(self, new_final_balance: int):
        Validator.validate(new_final_balance, type_=int)
        self.__final_balance = new_final_balance

    def local_eq(self, other):
        return self.nomenclature_name == other.nomenclature_name

    @classmethod
    def from_dict(cls, data: dict):
        Validator.check_fields(data=data, model=cls)
        item = cls()
        item.nomenclature_name = data["nomenclature_name"]
        item.initial_balance = data["initial_balance"]
        item.turnover = data["turnover"]
        item.final_balance = data["final_balance"]
        return item

    @staticmethod
    def create(nomenclature_name: str, initial_balance: int, turnover: int, final_balance: int) -> 'OSV':
        # Validate
        Validator.validate(nomenclature_name, type_=str)
        Validator.validate(initial_balance, type_=int)
        Validator.validate(turnover, type_=int)
        Validator.validate(final_balance, type_=int)
        # Factory method
        item = OSV()
        item.nomenclature_name = nomenclature_name
        item.initial_balance = initial_balance
        item.turnover = turnover
        item.final_balance = final_balance
        return item
