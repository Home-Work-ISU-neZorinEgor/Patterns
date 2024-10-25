import os.path

from src.storage import DataStorage
from src.models.settings import Settings
from src.settings_manager import SettingsManager
from src.service.starter import StartService


def get_settings() -> Settings:
    manager = SettingsManager()
    manager.from_json(os.path.join("settings.json"))
    return manager.settings


def get_storage() -> DataStorage:
    storage = DataStorage()
    start_service = StartService(storage)
    start_service.create()
    return storage
