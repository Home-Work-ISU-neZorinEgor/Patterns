from abc import ABC, abstractmethod
from typing import List


class TransactionProcessor(ABC):
    @abstractmethod
    def preprocess(self, transaction: List):
        pass
