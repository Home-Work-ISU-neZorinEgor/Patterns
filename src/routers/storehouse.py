import datetime

from fastapi import APIRouter, Depends
from typing import Optional, List

from src.dependency import DependencyContainer
from src.models.settings import Settings
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
    return StorehouseService.stock_count(transactions)


@router.post("/set_block_time", status_code=200)
def set_block_time(
        new_block_time: float = datetime.datetime.now(datetime.UTC).timestamp(),
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    return StorehouseService(storage=storage, settings=settings).set_block_time(new_block_time)
