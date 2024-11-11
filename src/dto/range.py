from typing import Optional

from src.dto.base import BaseModelDTO


class RangeDTO(BaseModelDTO):
    name: str
    conversion_factor: int | float
    base_unit: Optional['RangeDTO']

