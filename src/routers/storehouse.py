import datetime
import json

from fastapi import APIRouter, Depends
from typing import Optional, List

from src.dependency import DependencyContainer
from src.models.settings import Settings
from src.reports.json_report import JSONReport
from src.service.storehouse import StorehouseService
from src.storage import DataStorage

router = APIRouter(prefix="/storehouse", tags=["Storehouse"])


@router.get("/get_transaction")
def get_storehouse_transaction(
        field: Optional[str] = None,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    return StorehouseService(settings=settings, storage=storage).get_transaction(sort_by=field)


@router.get("/osv")
def calculate_osv(
        datetime_start: float,
        datetime_end: float,
        storehouse_uuid: str,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    return [json.loads(JSONReport().create(o)) for o in StorehouseService.calculate_osv(
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        storehouse_uuid=storehouse_uuid,
        block_time=settings.block_time,
        transactions=storage.data[DataStorage.transaction_id()]
    )]


@router.post("/stock_count")
def stock_count(
        user_block_time: Optional[bool] | None,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    return StorehouseService.stock_count(
        transactions=storage.data[DataStorage.transaction_id()],
        user_block_time=user_block_time,
        block_time=settings.block_time,
    )


@router.post("/set_block_time", status_code=200)
def set_block_time(
        new_block_time: float = datetime.datetime.now(datetime.UTC).timestamp(),
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):

    return StorehouseService(storage=storage, settings=settings).set_block_time(new_block_time)


@router.get("/get_block_time", status_code=200)
def get_block_time(
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    return StorehouseService(storage=storage, settings=settings).get_block_time()
