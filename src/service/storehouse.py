import json
from typing import List

from src.models.settings import Settings
from src.models.storehouse_transaction import StorehouseTransaction
from src.models.turnhover_calculator import TurnoverCalculator
from src.reports.factory import ReportFactory
from src.storage import DataStorage


class StorehouseService:
    def __init__(self, storage: DataStorage, settings: Settings):
        self.storage = storage
        self.settings = settings
        self.factory = ReportFactory(self.settings).create_default()

    def get_transaction(self, sort_by: str):
        transaction = self.storage.data[DataStorage.transaction_id()]
        transaction_report = list(map(self.factory.create, transaction))
        return list(map(json.loads, transaction_report))

    @staticmethod
    def stock_count(transactions: List[dict]):
        transactions = list(map(StorehouseTransaction.from_dict, transactions))
        return TurnoverCalculator().stock_count(transactions=transactions)


