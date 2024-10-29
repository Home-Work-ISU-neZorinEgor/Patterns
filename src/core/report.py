from abc import ABC, abstractmethod
from enum import IntEnum
from datetime import datetime


class ReportFormatEnum(IntEnum):
    CSV = 1
    MARKDOWN = 2
    JSON = 3
    XML = 4
    RTF = 5


class ABCReport(ABC):
    """
    Абстрактный класс для отчётов
    """
    __format: ReportFormatEnum = ReportFormatEnum.CSV

    @abstractmethod
    def create(self, data):
        pass

    def _to_serializable(self, val):
        """
        Вспомогательная функция для рекурсивного преобразования объектов в строковые представления
        """
        if isinstance(val, dict):
            return {str(k): self._to_serializable(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [self._to_serializable(v) for v in val]
        elif isinstance(val, (int, float, bool)):  # Числовые и логические типы оставляем как есть
            return val
        elif isinstance(val, datetime):   # timestamp
            return val.timestamp()
        elif hasattr(val, '__dict__'):
            fields = list(filter(lambda x: not x.startswith("_"), dir(val)))
            return {field: self._to_serializable(getattr(val, field)) for field in fields if
                    not callable(getattr(val, field))}
        elif val is None:  # null
            return None
        return str(val)

    @property
    def format(self):
        return self.__format
