from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routers.reports import router as report_router
from src.routers.storehouse import router as storehouse_router


@asynccontextmanager
async def lifespan(instance: FastAPI):
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
