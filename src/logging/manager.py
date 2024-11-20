import datetime

from src.logging.level import LogLevel
from src.logging.logger import _Logger
from src.settings_manager import SettingsManager
from src.utils.validator import Validator


class LoggerManager:
    __instance = None
    __level: LogLevel = None
    __timezone: datetime.timezone = None
    __file: str = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(LoggerManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, level: LogLevel):
        Validator.validate(level, type_=LogLevel)
        self.__level = level

    def configure(self, timezone: datetime.timezone = datetime.timezone.utc, file: str = None):
        Validator.validate(timezone, type_=datetime.timezone)
        Validator.validate(file, type_=str | None)
        self.__timezone = timezone
        self.__file = file

    def logger(self, name) -> _Logger:
        Validator.validate(name, type_=str)
        return _Logger(timezone=self.__timezone, level=self.__level, name=name, file=self.__file)


logger_manager = LoggerManager(level=LogLevel(SettingsManager().settings.logging_level))
logger_manager.configure(timezone=datetime.timezone.utc)
