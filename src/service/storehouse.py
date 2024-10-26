import json

from src.models.settings import Settings
from src.reports.factory import ReportFactory
from src.storage import DataStorage


class StorehouseService:
    def __init__(self, storage: DataStorage, settings: Settings):
        self.storage = storage
        self.settings = settings
        self.factory = ReportFactory(self.settings).create_default()

    def get_transaction(self):
        transaction = self.storage.data[DataStorage.transaction_id()]
        transaction_report = list(map(self.factory.create, transaction))
        return list(map(json.loads, transaction_report))
