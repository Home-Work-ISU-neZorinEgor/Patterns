from typing import List

from src.core.transaction import TransactionProcessor
from src.models.storehose_turnover import StorehouseTurnover
from src.models.storehouse_transaction import TransactionType, StorehouseTransaction


class TurnoverCalculator(TransactionProcessor):
    def preprocess(self, transactions: List[StorehouseTransaction], start_date: datetime.datetime,
                end_date: datetime.datetime) -> List[StorehouseTurnover]:
        turnover_data = {}

        # Фильтруем транзакции по дате
        filtered_transactions = [t for t in transactions if start_date <= t.time <= end_date]

        # Рассчитываем обороты
        for transaction in filtered_transactions:
            key = (transaction.storehouse, transaction.nomenclature, transaction.range)
            turnover_change = transaction.quantity if transaction.transaction_type == TransactionType.INBOUND else -transaction.quantity

            if key not in turnover_data:
                turnover_data[key] = StorehouseTurnover(
                    storehouse=transaction.storehouse,
                    turnover=0,
                    nomenclature=transaction.nomenclature,
                    range=transaction.range
                )
            turnover_data[key].turnover += turnover_change

        return list(turnover_data.values())