from abc import ABC, abstractmethod
from typing import List

from src.models.storehouse_transaction import StorehouseTransaction


class TransactionProcessor(ABC):
    @abstractmethod
    def preprocess(self, transactions: List[StorehouseTransaction]):
        pass
