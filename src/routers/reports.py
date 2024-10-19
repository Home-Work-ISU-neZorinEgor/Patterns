from fastapi import APIRouter
from src.core.report import FormatEnum
from typing import Dict

from src.report_factory import ReportFactory
from src.settings_manager import SettingsManager

router = APIRouter(tags=["Reports"], prefix="/report")


@router.get("/formats")
def get_reports_formats() -> Dict:
    return {
        "ok": True,
        "formats": [enum.name for enum in FormatEnum]
    }


@router.post("/create")
def generate_report(report_format: FormatEnum, obj_dict: Dict):
    manager = SettingsManager()
    manager.from_json("../settings.json")
    report_factory = ReportFactory(manager.settings)
    reporter = report_factory.create(report_format.value)
    return {
        "ok": True,
        "report": reporter.create()
    }
