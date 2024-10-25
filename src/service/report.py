import json

from fastapi import Depends

from src.core.report import ReportFormatEnum
from src.dependency import get_settings, get_storage
from src.exceptions.http import ModelNotFounded
from src.models.settings import Settings
from src.reports.factory import ReportFactory
from src.storage import DataStorage


class ReportService:
    def __init__(self, storage: DataStorage):
        self.storage = storage

    @staticmethod
    def get_report_formats() -> dict[str, list[str]]:
        formats = [i.name for i in ReportFormatEnum]
        return {
            "formats": formats,
        }

    def generate_report(
            self,
            model: str,
            report_format: ReportFormatEnum,
            settings: Settings = Depends(get_settings),
    ):
        if not model.lower() in self.storage.data.keys():
            raise ModelNotFounded(model)
        factory = ReportFactory(settings)
        models = self.storage.data[model.lower()]
        report = list(map(factory.create(report_format).create, models))
        if report_format is ReportFormatEnum.JSON:
            return list(map(json.loads, report))
        return report
