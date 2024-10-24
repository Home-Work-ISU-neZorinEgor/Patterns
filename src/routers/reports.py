from typing import Dict, List

from fastapi import APIRouter

from src.core.report import FormatEnum

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/")
def get_formats() -> dict[str, list[str]]:
    formats = [i.name for i in FormatEnum]
    return {
        "formats": formats,
    }



