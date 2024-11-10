import os.path

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routers.reports import router as report_router
from src.routers.storehouse import router as storehouse_router
from src.routers.nomenclature import router as nomenclature_router

from src.settings_manager import SettingsManager


@asynccontextmanager
async def lifespan(instance: FastAPI):
    manager = SettingsManager()
    manager.from_json(os.path.join("settings.json"))
    yield


app = FastAPI(
    docs_url="/docs",
    title="Система финансового учёта",
    description="### Проект по предмету `Шаблоны проектирования`",
    lifespan=lifespan,
    version="1.0",
)


app.include_router(storehouse_router)
app.include_router(report_router)
app.include_router(nomenclature_router)
