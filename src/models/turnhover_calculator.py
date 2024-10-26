from typing import List

from src.core.transaction import TransactionProcessor
from src.models.storehose_turnover import StorehouseTurnover
from src.models.storehouse_transaction import TransactionType, StorehouseTransaction


class TurnoverCalculator(TransactionProcessor):
    def preprocess(self, transactions: List[StorehouseTransaction]) -> List[StorehouseTurnover]:
        # Словарь для хранения оборотов по каждому складу
        turnover_data = {}

        # Обрабатываем каждую транзакцию
        for transaction in transactions:
            storehouse = transaction.storehouse
            turnover_change = transaction.quantity if transaction.transaction_type == TransactionType.INBOUND else -transaction.quantity

            if storehouse not in turnover_data:
                turnover_data[storehouse] = StorehouseTurnover.create(
                    storehouse=storehouse,
                    turnover=0,
                    nomenclature=transaction.nomenclature,
                    range=transaction.range
                )
            turnover_data[storehouse].turnover += turnover_change

        return list(turnover_data.values())
