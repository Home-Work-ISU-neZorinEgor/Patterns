import os.path

from src.storage import DataStorage
from src.models.settings import Settings
from src.settings_manager import SettingsManager
from src.service.starter import StartService


class DependencyContainer:
    """
    Класс, возвращающий бины

    See: https://docs.spring.io/spring-framework/docs/6.1.14/javadoc-api/org/springframework/beans/factory/BeanFactory.html
    """
    @staticmethod
    def settings() -> Settings:
        manager = SettingsManager()
        manager.from_json(os.path.join("settings.json"))
        return manager.settings

    @staticmethod
    def storage() -> DataStorage:
        storage = DataStorage()
        start_service = StartService(storage)
        start_service.create()
        return storage