import datetime
import json
from typing import List, Dict, Optional
from src.core.transaction import TransactionProcessor
from src.models.storehose_turnover import StorehouseTurnover
from src.models.storehouse_transaction import TransactionType, StorehouseTransaction
from src.reports.json_report import JSONReport


class TurnoverCalculator(TransactionProcessor):
    @staticmethod
    def stock_count(transactions: List[StorehouseTransaction], block_time: float, user_block_time: Optional[float] = None) -> List[StorehouseTurnover]:
        storehouse_turnover: Dict[tuple, int] = {}
        print(transactions[0].time.timestamp())
        print(bool(user_block_time))
        # Рассчитываем обороты по каждой транзакции с учетом use_block_time
        for transaction in transactions:
            if user_block_time and transaction.time.timestamp() > block_time:
                continue  # Пропускаем транзакции после use_block_time

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
                range=transaction.range  # Передаем экземпляр единицы измерения
            )
            for key, turnover in storehouse_turnover.items()
        ]

        # Возвращаем JSON-отчет для всех записей оборота
        return list(map(json.loads, list(map(JSONReport().create, result))))