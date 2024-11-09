import json

from src.models.nomenclature import Nomenclature
from src.models.settings import Settings
from src.reports.factory import ReportFactory
from src.storage import DataStorage


class NomenclatureService:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(NomenclatureService, cls).__new__(cls)
        return cls.__instance

    def __init__(self, storage: DataStorage | None, settings: Settings | None):
        if not hasattr(self, "initialized"):
            self.storage = storage
            self.settings = settings
            self.factory = ReportFactory(self.settings).create_default()
            self.initialized = True  # Флаг для предотвращения повторной инициализации

    def get_nomenclature_by_uuid(self, uuid: str):
        nomenclatures = [self.factory.create(i) for i in self.storage.data[DataStorage.nomenclature_id()] if i.uuid == uuid]
        print(nomenclatures)
        return [json.loads(n) for n in nomenclatures]

    def get_all_nomenclature(self):
        return [json.loads(n) for n in [self.factory.create(i) for i in self.storage.data[DataStorage.nomenclature_id()] if i.uuid]]

    def add_nomenclature(self, nomenclature: dict):
        self.storage.data[DataStorage.nomenclature_id()].append(Nomenclature.from_dict(nomenclature))
        return len(self.storage.data[DataStorage.nomenclature_id()])

    def delete_nomenclature_by_uuid(self, uuid: str):
        self.storage.data[DataStorage.nomenclature_id()] = [i for i in self.storage.data[DataStorage.nomenclature_id()] if i.uuid != uuid]
        return "ok"

    def update_nomenclature(self, nomenclature: dict):
        idx = None
        for index, i in enumerate(self.storage.data[DataStorage.nomenclature_id()]):
            if i.uuid == nomenclature["uuid"]:
                idx = index
        update_nomenclature = Nomenclature.from_dict(nomenclature)
        self.storage.data[DataStorage.nomenclature_id()][idx] = update_nomenclature
