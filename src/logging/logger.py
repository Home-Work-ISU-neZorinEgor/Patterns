import datetime
from typing import Callable

from src.logging.level import LogLevel
from src.utils.validator import Validator


class _Logger:
    __timezone: datetime.timezone = None
    __level: LogLevel = None
    __name: str = None

    def __init__(self, timezone, level, name):
        Validator.validate(timezone, type_=datetime.timezone)
        Validator.validate(level, type_=LogLevel)
        Validator.validate(name, type_=str)
        self.__timezone = timezone
        self.__level = level
        self.__name = name

    def debug(self, message: str, level=LogLevel.DEBUG):
        if self.__level.value > level.value:
            pass
        else:
            Validator.validate(message, type_=str)
            print(f"[{datetime.datetime.now(self.__timezone)}] - {self.__name} - {level.name} - {message}")

    def info(self, message: str, level=LogLevel.INFO):
        if self.__level.value > level.value:
            pass
        else:
            Validator.validate(message, type_=str)
            print(f"[{datetime.datetime.now(self.__timezone)}] - {self.__name} - {level.name} - {message}")

    def error(self, message: str, level=LogLevel.ERROR):
        if self.__level.value > level.value:
            pass
        else:
            Validator.validate(message, type_=str)
            print(f"[{datetime.datetime.now(self.__timezone)}] - {self.__name} - {level.name} - {message}")

