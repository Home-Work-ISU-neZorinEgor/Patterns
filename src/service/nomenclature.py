import json

from fastapi import HTTPException

from src.models.nomenclature import Nomenclature
from src.models.settings import Settings
from src.reports.factory import ReportFactory
from src.storage import DataStorage


class NomenclatureService:
    not_founded_by_uuid_exceptions = HTTPException(status_code=404, detail="Nomenclature by this uuid not founded.")

    def __init__(self, storage: DataStorage | None, settings: Settings | None):
        self.storage = storage
        self.settings = settings
        self.factory = ReportFactory(self.settings).create_default()

    def get_nomenclature_by_uuid(self, uuid: str):
        nomenclatures = [self.factory.create(i) for i in self.storage.data[DataStorage.nomenclature_id()] if i.uuid == uuid]
        if not nomenclatures:
            raise self.not_founded_by_uuid_exceptions
        return [json.loads(n) for n in nomenclatures]

    def get_all_nomenclature(self):
        return [json.loads(n) for n in [self.factory.create(i) for i in self.storage.data[DataStorage.nomenclature_id()] if i.uuid]]

    def add_nomenclature(self, nomenclature: dict):
        self.storage.data[DataStorage.nomenclature_id()].append(Nomenclature.from_dict(nomenclature))
        return len(self.storage.data[DataStorage.nomenclature_id()])

    def delete_nomenclature_by_uuid(self, uuid: str):
        start_len = self.storage.data[DataStorage.nomenclature_id()]
        self.storage.data[DataStorage.nomenclature_id()] = [i for i in self.storage.data[DataStorage.nomenclature_id()] if i.uuid != uuid]
        if start_len == len(self.storage.data[DataStorage.nomenclature_id()]):
            raise self.not_founded_by_uuid_exceptions
        return "ok"

    def update_nomenclature(self, nomenclature: dict):
        idx = None
        for index, i in enumerate(self.storage.data[DataStorage.nomenclature_id()]):
            if i.uuid == nomenclature["uuid"]:
                idx = index
        if idx is None:
            raise self.not_founded_by_uuid_exceptions
        update_nomenclature = Nomenclature.from_dict(nomenclature)
        self.storage.data[DataStorage.nomenclature_id()][idx] = update_nomenclature
