import datetime
from enum import Enum

from src.core.model import BaseModel
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.storehouse_transaction import Storehouse
from src.utils.validator import Validator


class TransactionType(Enum):
    INBOUND = 0
    OUTBOUND = 1


class StorehouseTransaction(BaseModel):
    __storehouse: Storehouse = None
    __nomenclature: Nomenclature = None
    __quantity: int = None
    __transaction_type: TransactionType = None
    __range: Range = None
    __time: datetime.datetime = None

    @property
    def storehouse(self):
        return self.__storehouse

    @storehouse.setter
    def storehouse(self, new_storehouse):
        Validator.validate(new_storehouse, type_=Storehouse)
        self.__storehouse = new_storehouse

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
        Validator.validate(new_quantity, type_=int)
        self.__quantity = new_quantity

    @property
    def transaction_type(self):
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, new_transaction_type):
        Validator.validate(new_transaction_type, type_=TransactionType)
        self.__transaction_type = new_transaction_type

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, new_range):
        Validator.validate(new_range, type_=Range)
        self.__range = new_range

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, new_time):
        Validator.validate(new_time, type_=datetime.datetime)
        self.__time = new_time

    @staticmethod
    def create(storehouse, nomenclature, quantity, range, time) -> 'StorehouseTransaction':
        Validator.validate(storehouse, type_=Storehouse)
        Validator.validate(nomenclature, type_=Nomenclature)
        Validator.validate(quantity, type_=int)
        Validator.validate(range, type_=Range)
        Validator.validate(time, type_=datetime.datetime)

        transaction = StorehouseTransaction()
        transaction.storehouse = storehouse
        transaction.nomenclature = nomenclature
        transaction.quantity = quantity,
        transaction.range = range
        transaction.time = time
        return transaction

    def local_eq(self, other):
        pass
