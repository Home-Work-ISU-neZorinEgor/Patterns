import json
from datetime import datetime
from typing import List, Optional

from src.models.settings import Settings
from src.models.storehouse_transaction import StorehouseTransaction
from src.models.turnhover_calculator import TurnoverCalculator
from src.reports.factory import ReportFactory
from src.settings_manager import SettingsManager
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
        return TurnoverCalculator.stock_count(transactions, user_block_time=user_block_time, block_time=block_time)

    def set_block_time(self, new_block_time) -> dict:
        old = SettingsManager().settings.block_time
        SettingsManager().settings.block_time = new_block_time
        return {
            "ok": True,
            "old_time": old,
            "new_time": self.settings.block_time
        }

    def get_block_time(self):
        return self.settings.block_time

    @staticmethod
    def osv(datetime_start: float, datetime_end: float, address: str, block_time: float, transactions: List[StorehouseTransaction]):
        # Фильтрация транзакций по временному диапазону
        relevant_transactions = [
            t for t in transactions
            if t.storehouse.address == address and datetime_start <= t.time.timestamp() <= datetime_end
        ]

        # Вычисление оборотов (использование уже существующего метода с фильтрованными транзакциями)
        turnover_data = StorehouseService.stock_count(
            transactions=relevant_transactions,
            user_block_time=False,
            block_time=block_time,
        )

        # Расчёт начального остатка по транзакциям до datetime_start
        initial_balance = {}
        for t in transactions:
            if t.storehouse.address == address and t.time.timestamp() < datetime_start:
                nomenclature = t['nomenclature']['name']
                quantity = t.quantity if t.transaction_type.value == 'INBOUND' else -t.quantity
                initial_balance[nomenclature] = initial_balance.get(nomenclature, 0) + quantity

        # Создание ОСВ
        osv = []
        for t in turnover_data:
            nomenclature = t['nomenclature']['name']
            turnover = t['turnover']
            initial = initial_balance.get(nomenclature, 0)
            final_balance = initial + turnover
            osv.append({
                "nomenclature": nomenclature,
                "initial_balance": initial,
                "turnover": turnover,
                "final_balance": final_balance
            })

        return osv
