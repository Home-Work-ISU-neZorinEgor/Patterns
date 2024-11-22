import datetime

from src.core.model import BaseModel
from src.core.observable import Observable, EventType, Subject
from src.logging.level import LogLevel
from src.logging.logger import _Logger
from src.settings_manager import SettingsManager
from src.utils.validator import Validator


class LoggerManager(Observable):
    def check_statement(self, event_type: EventType, entity: BaseModel):
        match event_type:
            case event_type.DELETE_NOMENCLATURE:
                self.logger(__name__).info("Номенклатура удалена")
            case event_type.UPDATE_NOMENCLATURE:
                self.logger(__name__).info("Номенклатура обновлена")
            case event_type.ON_SAVE_DUMP:
                self.logger(__name__).info("Save data at dump.")

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
logging_subject = Subject()
logging_subject.attach(logger_manager)
