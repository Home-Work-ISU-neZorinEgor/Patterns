import datetime
import json
from typing import List, Dict
from src.core.transaction import TransactionProcessor
from src.models.storehose_turnover import StorehouseTurnover
from src.models.storehouse_transaction import TransactionType, StorehouseTransaction
from src.reports.json_report import JSONReport


class TurnoverCalculator(TransactionProcessor):
    @staticmethod
    def stock_time_before_block_time(transactions: List[StorehouseTransaction], block_time: float):
        storehouse_turnover: Dict[tuple, int] = {}

        # Рассчитываем обороты по каждой транзакции до даты блокировки
        for transaction in transactions:
            if transaction.time.timestamp() > block_time:
                continue  # Пропускаем транзакции после block_period

            key = (transaction.storehouse.uuid, transaction.nomenclature.uuid, transaction.range.uuid)

            # Определяем количество в зависимости от типа транзакции
            if transaction.transaction_type == TransactionType.INBOUND:
                storehouse_turnover[key] = storehouse_turnover.get(key, 0) + transaction.quantity
            elif transaction.transaction_type == TransactionType.OUTBOUND:
                storehouse_turnover[key] = storehouse_turnover.get(key, 0) - transaction.quantity

        # Создаем список StorehouseTurnover на основании накопленных данных
        result = [
            StorehouseTurnover.create(
                storehouse=transaction.storehouse,  # Передаем экземпляр склада
                turnover=turnover,
                nomenclature=transaction.nomenclature,  # Передаем экземпляр номенклатуры
                range=transaction.range,  # Передаем экземпляр единицы измерения
            )
            for key, turnover in storehouse_turnover.items()
        ]

        # Возвращаем JSON-отчет для всех записей оборота
        return list(map(json.loads, list(map(JSONReport().create, result))))

    @staticmethod
    def stock_count(transactions: List[StorehouseTransaction]) -> List[StorehouseTurnover]:
        storehouse_turnover: Dict[tuple, int] = {}

        # Рассчитываем обороты по каждой транзакции
        for transaction in transactions:
            key = (transaction.storehouse.uuid, transaction.nomenclature.uuid, transaction.range.uuid)

            # Определяем количество в зависимости от типа транзакции
            if transaction.transaction_type == TransactionType.INBOUND:
                storehouse_turnover[key] = storehouse_turnover.get(key, 0) + transaction.quantity
            elif transaction.transaction_type == TransactionType.OUTBOUND:
                storehouse_turnover[key] = storehouse_turnover.get(key, 0) - transaction.quantity

        # Создаем список StorehouseTurnover на основании накопленных данных
        result = [
            StorehouseTurnover.create(
                storehouse=transaction.storehouse,  # Передаем экземпляр, а не UUID
                turnover=turnover,
                nomenclature=transaction.nomenclature,  # Передаем экземпляр, а не UUID
                range=transaction.range  # Передаем экземпляр, а не UUID
            )
            for key, turnover in storehouse_turnover.items()
            if transaction.nomenclature and transaction.range  # Проверяем наличие nomenclature и range
        ]

        return list(map(json.loads, list(map(JSONReport().create, result))))
