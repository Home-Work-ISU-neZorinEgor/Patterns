from src.dto.base import BaseModelDTO
from src.dto.group_nomenclature import NomenclatureGroupDTO
from src.dto.range import RangeDTO


class NomenclatureDTO(BaseModelDTO):
    group: NomenclatureGroupDTO
    name: str
    range: RangeDTO


