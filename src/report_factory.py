from src.core.report import FormatEnum
from src.errors.custom import InvalidType
from src.errors.proxy import ErrorProxy
from src.utils.validator import Validator
from src.models.settings import Settings


class ReportFactory:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.error_proxy = ErrorProxy()
        self.report_classes = settings.report_classes

    def create(self, report_format: FormatEnum):
        """
        Возвращает класс, в зависимости от входного аргумента
        """
        Validator.validate(report_format, FormatEnum)

        report_class = self.report_classes.get(report_format)
        if report_class is None:
            raise InvalidType("Неподдерживаемый формат отчета")

        return report_class()

    def create_default(self):
        """
        Возвращает класс в зависимости от значения по умолчанию из настроек
        """
        base_format = self.settings.report_format
        report_class = self.report_classes.get(base_format)
        if report_class is None:
            raise InvalidType("Неподдерживаемый формат отчета")
        return report_class()
