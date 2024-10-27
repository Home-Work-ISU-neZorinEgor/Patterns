from typing import Optional, List

from fastapi import APIRouter, Depends

from src.dependency import DependencyContainer
from src.models.settings import Settings
from src.models.storehouse_transaction import StorehouseTransaction, TransactionType
from src.models.turnhover_calculator import TurnoverCalculator
from src.service.storehouse import StorehouseService
from src.storage import DataStorage

router = APIRouter(prefix="/storehouse", tags=["Storehouse"])


@router.get("/")
def get_storehouse_transaction(
        field: Optional[str] = None,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    return StorehouseService(settings=settings, storage=storage).get_transaction(sort_by=field)


@router.post("/stock_count")
def stock_count(transactions: List[dict]):
    transactions_lst = list(map(StorehouseTransaction.from_dict, transactions))
    return TurnoverCalculator().stock_count(transactions_lst)
    # print(turnover)
