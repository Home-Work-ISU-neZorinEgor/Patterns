from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routers.reports import router as report_format
from src.routers.storehouse_transaction import router as storehouse_router


@asynccontextmanager
async def lifespan(instance: FastAPI):
    yield


app = FastAPI(
    docs_url="/docs",
    title="Patterns Tasks",
    lifespan=lifespan,
)

app.include_router(storehouse_router)
app.include_router(report_format)
