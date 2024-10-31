from abc import ABC, abstractmethod
from typing import List
import datetime
from src.models.storehouse_transaction import StorehouseTransaction, TransactionType


class TransactionProcessor(ABC):
    @staticmethod
    @abstractmethod
    def stock_count(transactions: List[StorehouseTransaction]):
        raise NotImplemented()

    @staticmethod
    @abstractmethod
    def stock_time_before_block_time(
            transactions: List[StorehouseTransaction], block_time: float
    ):
        raise NotImplemented()
