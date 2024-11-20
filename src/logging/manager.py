import datetime

from src.logging.level import LogLevel
from src.logging.logger import _Logger
from src.utils.validator import Validator


class LoggerManager:
    __instance = None
    __level: LogLevel = None
    __timezone: datetime.timezone = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(LoggerManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, level: LogLevel):
        Validator.validate(level, type_=LogLevel)
        self.__level = level

    def configure(self, timezone: datetime.timezone):
        Validator.validate(timezone, type_=datetime.timezone)
        self.__timezone = timezone

    def logger(self, name) -> _Logger:
        Validator.validate(name, type_=str)
        return _Logger(timezone=self.__timezone, level=self.__level, name=name)


logger_manager = LoggerManager(level=LogLevel.INFO)
logger_manager.configure(timezone=datetime.timezone.utc)
logger = logger_manager.logger(__name__)
logger.info(message="LOG!")
logger.debug(message="LOG!")
logger.error(message="LOG!")
