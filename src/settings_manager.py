import json
import os

from src.core.report import ReportFormatEnum
from src.exceptions.proxy import ErrorProxy
from src.exceptions.custom import InvalidTypeException, UnsupportableReportFormatException
from src.models.settings import Settings


class SettingsManager:
    """Класс для управления настройками с интеграцией ErrorProxy."""

    file_name = "settings.json"
    __settings = Settings()
    __error_proxy = ErrorProxy()
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SettingsManager, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def error_proxy(self) -> ErrorProxy:
        return self.__error_proxy

    def set_exception(self, ex: Exception) -> None:
        """Устанавливает сообщение об ошибке в ErrorProxy."""
        self.__error_proxy.error_message = str(ex)
        raise ex

    def from_json(self, path: str = os.path.join(os.pardir, 'settings.json')) -> None:
        """Загрузка настроек из JSON файла."""
        try:
            if not isinstance(path, str):
                raise InvalidTypeException("File path should be a string")
            if not os.path.exists(path):
                raise FileNotFoundError(f"File {path} does not exist")

            with open(path, "r", encoding="utf-8") as f:
                file = json.load(f)
                for key, value in file.items():
                    if hasattr(self.__settings, key):
                        if key == "report_format":
                            if value in ReportFormatEnum._value2member_map_:
                                setattr(self.__settings, key, ReportFormatEnum(value))
                            else:
                                raise UnsupportableReportFormatException(f"Invalid value for report_format: {value}")
                        else:
                            setattr(self.__settings, key, value)
        except Exception as ex:
            self.set_exception(ex)

    def from_dict(self, input_dict: dict) -> None:
        """Установка полей класса Settings из dict'а."""
        try:
            if not isinstance(input_dict, dict):
                raise InvalidTypeException("Var should be a dict")

            for key, value in input_dict.items():
                if hasattr(self.__settings, key):
                    setattr(self.__settings, key, value)
        except Exception as ex:
            self.set_exception(ex)
