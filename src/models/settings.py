import datetime

from src.core.report import ReportFormatEnum
from src.exceptions.custom import InvalidTypeException, InvalidLengthException
from src.utils.validator import Validator
from src.reports.csv_report import CSVReport
from src.reports.json_report import JSONReport
from src.reports.markdown_report import MarkdownReport
from src.reports.rtf_report import RTFReport
from src.reports.xml_report import XMLReport


class Settings:
    """Модель настроек с кастомными ошибками."""
    __path_to_settings_file: str = ""
    __inn: str = "Default value"
    __account: str = "Default value"
    __correspondent_account: str = "Default value"
    __bic: str = "Default value"
    __name: str = "Default value"
    __type_of_ownership: str = "Default value"
    __block_time: int | float = datetime.datetime.now(datetime.UTC).timestamp()
    __report_format: ReportFormatEnum = ReportFormatEnum.CSV
    __first_start_up: bool = True
    __logging_level: int = 0
    __report_classes = {
        ReportFormatEnum.CSV: CSVReport,
        ReportFormatEnum.MARKDOWN: MarkdownReport,
        ReportFormatEnum.JSON: JSONReport,
        ReportFormatEnum.XML: XMLReport,
        ReportFormatEnum.RTF: RTFReport,
    }

    @property
    def logging_level(self):
        return self.__logging_level

    @logging_level.setter
    def logging_level(self, new_logging_level):
        Validator.validate(new_logging_level, type_=int)
        self.__logging_level = new_logging_level

    @property
    def first_start_up(self):
        return self.__first_start_up

    @first_start_up.setter
    def first_start_up(self, new_first_start_up: bool):
        Validator.validate(new_first_start_up, type_=bool)
        self.__first_start_up = new_first_start_up

    @property
    def block_time(self):
        return self.__block_time

    @block_time.setter
    def block_time(self, new_block_time):
        Validator.validate(new_block_time, type_=int | float)
        self.__block_time = new_block_time

    @property
    def report_classes(self):
        return self.__report_classes

    @report_classes.setter
    def report_classes(self, class_mapping: dict) -> None:
        if not isinstance(class_mapping, dict):
            raise InvalidTypeException("report_classes must be a dictionary")
        self.__report_classes = class_mapping

    def __str__(self):
        return (f"INN: {self.__inn} \nACCOUNT: {self.__account} \n"
                f"CORRESPONDENT_ACCOUNT: {self.__correspondent_account} \n"
                f"BIC: {self.__bic} \nNAME: {self.__name} \n"
                f"TYPE_OF_OWNERSHIP: {self.__type_of_ownership}")

    @property
    def report_format(self) -> ReportFormatEnum:
        return self.__report_format

    @report_format.setter
    def report_format(self, new_format) -> None:
        Validator.validate(new_format, ReportFormatEnum)
        self.__report_format = new_format

    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, new_inn) -> None:
        if not isinstance(new_inn, str):
            raise InvalidTypeException("INN must be a string")
        if len(new_inn) != 12:
            raise InvalidLengthException(f"INN must be exactly 12 characters long, not {len(new_inn)}")
        self.__inn = new_inn

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, new_account) -> None:
        if not isinstance(new_account, str):
            raise InvalidTypeException("ACCOUNT must be a string")
        if len(new_account) != 11:
            raise InvalidLengthException(f"ACCOUNT must be exactly 11 characters long, not {len(new_account)}")
        self.__account = new_account

    @property
    def correspondent_account(self) -> str:
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, new_correspondent_account) -> None:
        if not isinstance(new_correspondent_account, str):
            raise InvalidTypeException("CORRESPONDENT_ACCOUNT must be a string")
        if len(new_correspondent_account) != 11:
            raise InvalidLengthException(
                f"CORRESPONDENT_ACCOUNT must be exactly 11 characters long, not {len(new_correspondent_account)}")
        self.__correspondent_account = new_correspondent_account

    @property
    def bic(self) -> str:
        return self.__bic

    @bic.setter
    def bic(self, new_bic) -> None:
        if not isinstance(new_bic, str):
            raise InvalidTypeException("BIC must be a string")
        if len(new_bic) != 9:
            raise InvalidLengthException(f"BIC must be exactly 9 characters long, not {len(new_bic)}")
        self.__bic = new_bic

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name) -> None:
        if not isinstance(new_name, str):
            raise InvalidTypeException("NAME must be a string")
        self.__name = new_name

    @property
    def type_of_ownership(self) -> str:
        return self.__type_of_ownership

    @property
    def path_to_settings_file(self):
        return self.__path_to_settings_file

    @path_to_settings_file.setter
    def path_to_settings_file(self, new_path_to_settings_file: str):
        self.__path_to_settings_file = new_path_to_settings_file

    @type_of_ownership.setter
    def type_of_ownership(self, new_type_of_ownership) -> None:
        if not isinstance(new_type_of_ownership, str):
            raise InvalidTypeException("TYPE_OF_OWNERSHIP must be a string")
        if len(new_type_of_ownership) != 5:
            raise InvalidLengthException(
                f"TYPE_OF_OWNERSHIP must be exactly 5 characters long, not {len(new_type_of_ownership)}")
        self.__type_of_ownership = new_type_of_ownership
