import json

from src.reports.json_report import JSONReport
from src.storage import DataStorage
from src.utils.validator import Validator


class DataDumpService:
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
        # dump_report
        with open(f"{dump_filename}.json", "w+") as f:
            f.write(json.dumps(dump_report, indent=4, ensure_ascii=False))

    def load_data_from_dump(self, file_content):
            return file_content
