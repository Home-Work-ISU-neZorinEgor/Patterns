import datetime

from src.dto.base import BaseModelDTO
from src.dto.nomenclature import NomenclatureDTO
from src.dto.range import RangeDTO
from src.dto.storehouse import StorehouseDTO
from src.dto.transaction_type import TransactionTypeDto


class TransactionDTO(BaseModelDTO):
    nomenclature: NomenclatureDTO
    quantity: int
    range: RangeDTO
    storehouse: StorehouseDTO
    time: float
    transaction_type: TransactionTypeDto


# print(TransactionDTO(
#     nomenclature=NomenclatureDTO(group=None, name=None, range=None),
#     quantity=10,
#     range=None,
#     storehouse=None,
#     time=datetime.datetime.now(datetime.UTC).timestamp(),
#     transaction_type=TransactionType.INBOUND
# ))
