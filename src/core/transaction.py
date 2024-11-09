from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.storehouse_transaction import StorehouseTransaction


class TransactionProcessor(ABC):
    @staticmethod
    @abstractmethod
    def stock_count(transactions: List[StorehouseTransaction], use_block_time: Optional[bool] | None):
        raise NotImplemented()
