from fastapi import APIRouter, Depends

from src.dependency import DependencyContainer
from src.models.settings import Settings
from src.service.nomenclature import NomenclatureService
from src.storage import DataStorage

router = APIRouter(prefix="/nomenclature", tags=["Nomenclature"])


@router.get("/{uuid}")
def get_nomenclature_by_uuid(
    uuid: str,
    storage: DataStorage = Depends(DependencyContainer.storage),
    settings: Settings = Depends(DependencyContainer.settings),
):
    return NomenclatureService(storage=storage, settings=settings).get_nomenclature_by_uuid(uuid)


@router.get("/")
def get_all_nomenclature(
    storage: DataStorage = Depends(DependencyContainer.storage),
    settings: Settings = Depends(DependencyContainer.settings),
):
    return NomenclatureService(storage=storage, settings=settings).get_all_nomenclature()


@router.post("/")
def add_nomenclature(
        nomenclature: dict,
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    return NomenclatureService(storage=storage, settings=settings).add_nomenclature(nomenclature)


@router.delete("/{uuid}")
def add_nomenclature(
        uuid: str,
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    return NomenclatureService(storage=storage, settings=settings).delete_nomenclature_by_uuid(uuid)


@router.patch("/")
def update_nomenclature(
        nomenclature: dict,
        storage: DataStorage = Depends(DependencyContainer.storage),
        settings: Settings = Depends(DependencyContainer.settings),
):
    return NomenclatureService(storage=storage, settings=settings).update_nomenclature(nomenclature)
