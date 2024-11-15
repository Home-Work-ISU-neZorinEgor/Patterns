import json
import os.path
from pathlib import Path

from fastapi import FastAPI, UploadFile
from contextlib import asynccontextmanager

from src.routers.reports import router as report_router
from src.routers.storehouse import router as storehouse_router
from src.routers.nomenclature import router as nomenclature_router
from src.routers.data_dump import router as data_dum_router
from src.service.data_dump import DataDumpService
from src.service.starter import StartService, data_storage

from src.settings_manager import SettingsManager


@asynccontextmanager
async def lifespan(instance: FastAPI):
    manager = SettingsManager()
    manager.from_json(os.path.join("settings.json"))
    start_service = StartService(data_storage)
    start_service.create()
    if not manager.settings.first_start_up:
        data_dump_path = open(os.path.join("dump.json"), "r")
        DataDumpService(data_storage).load_data_from_dump(json.loads(data_dump_path.read()))
    yield


app = FastAPI(
    docs_url="/docs",
    title="Система финансового учёта",
    description="### Проект по предмету `Шаблоны проектирования`",
    lifespan=lifespan,
    version="1.0",
)


app.include_router(nomenclature_router)
app.include_router(storehouse_router)
app.include_router(data_dum_router)
app.include_router(report_router)
