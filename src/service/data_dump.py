import json

from src.core.observer import Subject, EventType
from src.exceptions.http import ModelNotFounded
from src.models.group_nomenclature import GroupNomenclature
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.recipe import Recipe
from src.models.storehouse_transaction import StorehouseTransaction
from src.reports.json_report import JSONReport
from src.settings_manager import SettingsManager
from src.storage import DataStorage
from src.utils.validator import Validator

data_dump_subject = Subject()
data_dump_subject.attach(SettingsManager())


class DataDumpService:
    # TODO убрать в другое место
    MODEL_MAP = {
        "nomenclature": Nomenclature,
        "range": Range,
        "recipe": Recipe,
        "transaction": StorehouseTransaction,
        "group": GroupNomenclature,
    }

    def __init__(self, storage):
        Validator.validate(storage, type_=DataStorage)
        self.storage: DataStorage = storage

    def save_dump(self, dump_filename: str):
        dump_report = {}
        keys = [i for i in self.storage.data.keys()]
        for key in keys:
            if key not in dump_report:
                dump_report[key] = []
            for model in self.storage.data[key]:
                dump_report[key].append(json.loads(JSONReport().create(model)))
        with open(f"{dump_filename}.json", "w+") as f:
            f.write(json.dumps(dump_report, indent=4, ensure_ascii=False))

    def load_data_from_dump(self, file_content):
        for data_key, items in file_content.items():
            if not self.storage.data.get(data_key):
                raise ModelNotFounded(data_key)
            model_class = self.MODEL_MAP.get(data_key)
            if model_class and hasattr(model_class, 'from_dict'):
                for item in items:
                    self.storage.data[data_key].append(model_class.from_dict(item))
            data_dump_subject.notify(event_type=EventType.ON_SAVE_DUMP, entity=None)
        return f"Данные успешно загружены"
