import os.path

from src.storage import DataStorage
from src.models.settings import Settings
from src.settings_manager import SettingsManager
from src.service.starter import data_storage


class DependencyContainer:
    """
    Класс, возвращающий бины

    See: https://docs.spring.io/spring-framework/docs/6.1.14/javadoc-api/org/springframework/beans/factory/BeanFactory.html
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DependencyContainer, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @staticmethod
    def settings() -> Settings:
        manager = SettingsManager()
        manager.from_json(os.path.join("settings.json"))
        return manager.settings

    @staticmethod
    def storage() -> DataStorage:
        return data_storage
