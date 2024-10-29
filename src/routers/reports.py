from fastapi import APIRouter, Depends

from src.core.report import ReportFormatEnum
from src.dependency import DependencyContainer
from src.models.settings import Settings
from src.service.report import ReportService
from src.storage import DataStorage


router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/")
def get_report_formats() -> dict[str, list[str]]:
    return ReportService.get_report_formats()


@router.get("/get")
def generate_report(
        model: str,
        report_format: ReportFormatEnum,
        settings: Settings = Depends(DependencyContainer.settings),
        storage: DataStorage = Depends(DependencyContainer.storage),
):
    return ReportService(storage).generate_report(model, report_format, settings)
