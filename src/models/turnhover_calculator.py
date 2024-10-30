import json
from typing import List, Dict
from src.core.transaction import TransactionProcessor
from src.models.storehose_turnover import StorehouseTurnover
from src.models.storehouse_transaction import TransactionType, StorehouseTransaction
from src.reports.json_report import JSONReport


class TurnoverCalculator(TransactionProcessor):
    def stock_count(
            self, transactions: List[StorehouseTransaction],) -> List[StorehouseTurnover]:
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
