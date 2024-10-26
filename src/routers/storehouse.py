from typing import Optional

from fastapi import APIRouter, Depends

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
