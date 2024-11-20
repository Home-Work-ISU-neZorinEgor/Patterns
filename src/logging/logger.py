import datetime

from src.logging.level import LogLevel
from src.utils.validator import Validator


class _Logger:
    __timezone: datetime.timezone = None
    __level: LogLevel = None
    __name: str = None
    __file: str = None

    def __init__(self, timezone, level, name, file=None):
        Validator.validate(timezone, type_=datetime.timezone)
        Validator.validate(level, type_=LogLevel)
        Validator.validate(name, type_=str)
        if file is not None:
            Validator.validate(file, type_=str)
        self.__timezone = timezone
        self.__level = level
        self.__name = name
        self.__file = file

    def __write_log(self, message: str):
        """
        Вспомогательный метод для записи логов либо в файл, либо в консоль.
        """
        log_message = f"[{datetime.datetime.now(self.__timezone)}] - {self.__name} - {message}"

        if self.__file:
            # Если путь к файлу не None, записываем в файл
            with open(self.__file, 'a') as log_file:
                log_file.write(log_message + "\n")
        else:
            # Если __file равен None, выводим в консоль
            print(log_message)

    def debug(self, message: str, level=LogLevel.DEBUG):
        if self.__level.value <= level.value:
            Validator.validate(message, type_=str)
            self.__write_log(f"{level.name} - {message}")

    def info(self, message: str, level=LogLevel.INFO):
        if self.__level.value <= level.value:
            Validator.validate(message, type_=str)
            self.__write_log(f"{level.name} - {message}")

    def error(self, message: str, level=LogLevel.ERROR):
        if self.__level.value <= level.value:
            Validator.validate(message, type_=str)
            self.__write_log(f"{level.name} - {message}")
