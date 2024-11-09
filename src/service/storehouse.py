import json
from datetime import datetime
from typing import List, Optional

from src.models.settings import Settings
from src.models.storehouse_transaction import StorehouseTransaction
from src.models.turnhover_calculator import TurnoverCalculator
from src.reports.factory import ReportFactory
from src.storage import DataStorage


class StorehouseService:
    def __init__(self, storage: DataStorage | None, settings: Settings | None):
        self.storage = storage
        self.settings = settings
        self.factory = ReportFactory(self.settings).create_default()

    def get_transaction(self, sort_by: str):
        transaction = self.storage.data[DataStorage.transaction_id()]
        transaction_report = list(map(self.factory.create, transaction))
        return list(map(json.loads, transaction_report))

    @staticmethod

    def stock_count(transactions: List[StorehouseTransaction], user_block_time: Optional[bool] | None, block_time: float):
        return TurnoverCalculator.stock_count(transactions, use_block_time=user_block_time, block_time=block_time)

    def stock_count(transactions: List[dict]):
        transactions_lst = list(map(StorehouseTransaction.from_dict, transactions))
        return TurnoverCalculator().stock_count(transactions_lst)


    def set_block_time(self, new_block_time) -> dict:
        old = self.settings.block_time
        with open(self.settings.path_to_settings_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data["block_time"] = new_block_time
            f.seek(0)  # Перемещаем указатель в начало файла
            f.truncate()
            json.dump(data, f, ensure_ascii=False, indent=4)  # Перезаписываем файл с обновленными данными
        self.settings.block_time = new_block_time  # Обновляем текущее значение в настройках
        return {
            "ok": True,
            "old_time": old,
            "new_time": self.settings.block_time
        }


    def get_block_time(self):
        return self.settings.block_time



