import datetime
import json

from fastapi import APIRouter, Depends
from typing import Optional, List

from src.dependency import DependencyContainer
from src.models.settings import Settings
from src.reports.json_report import JSONReport
from src.service.storehouse import StorehouseService
from src.storage import DataStorage
from src.logging.manager import logger_manager

router = APIRouter(prefix="/storehouse", tags=["Storehouse"])
logger = logger_manager.logger(__name__)


@router.get("/get_transaction")
def get_storehouse_transaction(
        field: Optional[str] = None,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    logger.info(f"Получение транзакции с сортировкой по полю: {field}")
    result = StorehouseService(settings=settings, storage=storage).get_transaction(sort_by=field)
    logger.info(f"Транзакции получено: {len(result)}")
    return result


@router.get("/osv")
def calculate_osv(
        datetime_start: float,
        datetime_end: float,
        storehouse_uuid: str,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    logger.info(f"Расчет OSV с датами начала: {datetime_start} и конца: {datetime_end}, склад: {storehouse_uuid}")
    result = [
        json.loads(JSONReport().create(o)) for o in StorehouseService.calculate_osv(
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            storehouse_uuid=storehouse_uuid,
            block_time=settings.block_time,
            transactions=storage.data[DataStorage.transaction_id()]
        )
    ]
    logger.info(f"Расчет OSV завершен, количество записей: {len(result)}")
    return result


@router.post("/stock_count")
def stock_count(
        user_block_time: Optional[bool] | None,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    logger.info(f"Подсчет остатков с блокировкой пользователя: {user_block_time}")
    result = StorehouseService.stock_count(
        transactions=storage.data[DataStorage.transaction_id()],
        user_block_time=user_block_time,
        block_time=settings.block_time,
    )
    logger.info(f"Подсчет остатков завершен. Количество оборотов: {len(result)}")
    return result


@router.post("/set_block_time", status_code=200)
def set_block_time(
        new_block_time: float = datetime.datetime.now(datetime.UTC).timestamp(),
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    logger.info(f"Установка нового времени блокировки: {new_block_time}")
    result = StorehouseService(storage=storage, settings=settings).set_block_time(new_block_time)
    logger.info(f"Время блокировки успешно обновлено: {result}")
    return result


@router.get("/get_block_time", status_code=200)
def get_block_time(
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    logger.info("Получение текущего времени блокировки")
    result = StorehouseService(storage=storage, settings=settings).get_block_time()
    logger.info(f"Текущее время блокировки: {result}")
    return result
