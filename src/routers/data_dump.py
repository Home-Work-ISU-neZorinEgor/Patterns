from fastapi import APIRouter, Depends

from src.dependency import DependencyContainer
from src.service.data_dump import DataDumpService
from src.storage import DataStorage

router = APIRouter(prefix="/dump", tags=["Dump"])


@router.post("/save")
def save_dump(
        dump_filename: str = "dump",
        storage: DataStorage = Depends(DependencyContainer.storage)
):
    return DataDumpService(storage).save_dump(dump_filename)
