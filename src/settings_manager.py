import json
import os

from src.core.model import BaseModel
from src.core.observable import Observable, EventType
from src.core.report import ReportFormatEnum
from src.exceptions.proxy import ErrorProxy
from src.exceptions.custom import InvalidTypeException, UnsupportableReportFormatException
from src.models.settings import Settings
from src.reports.json_report import JSONReport


class SettingsManager(Observable):
    """Класс для управления настройками с интеграцией ErrorProxy."""

    def check_statement(self, event_type: EventType, entity: BaseModel):
        match event_type:
            case EventType.ON_SAVE_DUMP:
                self.__settings.first_start_up = False
                self.update_setting_in_file("first_start_up", False)

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
        self.settings.path_to_settings_file = os.path.abspath(path)
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

    def update_setting_in_file(self, key: str, value) -> None:
        """Обновляет значение настройки и сохраняет его в файле JSON."""
        try:
            # Проверяем, существует ли настройка с таким ключом
            if not hasattr(self.__settings, key):
                raise KeyError(f"Настройка '{key}' не найдена в Settings")

            # Обновляем значение в объекте настроек
            setattr(self.__settings, key, value)

            # Генерируем JSON-представление настроек
            settings_json = json.loads(JSONReport().create(self.__settings))
            # Удаляем поле 'report_classes', если оно существует
            settings_json.pop('report_classes', None)

            # Записываем обновленные настройки в JSON-файл
            with open(self.settings.path_to_settings_file, "w", encoding="utf-8") as f:
                json.dump(settings_json, f, indent=4, ensure_ascii=False)
        except Exception as ex:
            self.set_exception(ex)
