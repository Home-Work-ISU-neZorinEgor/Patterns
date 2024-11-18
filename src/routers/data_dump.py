import json

from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File

from src.core.observer import Subject
from src.dependency import DependencyContainer
from src.service.data_dump import DataDumpService
from src.storage import DataStorage

router = APIRouter(prefix="/dump", tags=["Dump"])


@router.post("/save")
def save_dump(
        background_task: BackgroundTasks,
        dump_filename: str = "dump",
        storage: DataStorage = Depends(DependencyContainer.storage)
):
    background_task.add_task(DataDumpService(storage).save_dump, dump_filename)
    return {
        "detail": f"save dump in: '{dump_filename}.json'"
    }


@router.post("/load_from_dump")
async def load_data_flom_dump(
    file: UploadFile = File(...),
    storage: DataStorage = Depends(DependencyContainer.storage)
):
    return DataDumpService(storage).load_data_from_dump(json.loads(await file.read()))
