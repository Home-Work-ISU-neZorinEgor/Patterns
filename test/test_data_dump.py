import json
import os

from src.service.data_dump import DataDumpService
from src.service.starter import data_storage
from src.settings_manager import SettingsManager
from src.storage import DataStorage


def test_load_data():
    SettingsManager().settings.first_start_up = True
    start_nom_len = len(data_storage.data[DataStorage.nomenclature_id()])
    data_dump_path = open(os.path.join(os.pardir, "dump.json"), "r")
    DataDumpService(data_storage).load_data_from_dump(json.loads(data_dump_path.read()))
    assert start_nom_len < len(data_storage.data[DataStorage.nomenclature_id()])
    assert SettingsManager().settings.first_start_up is False


def test_save_data():
    DataDumpService(data_storage).save_dump("magic_dump_name")
    assert os.path.exists("magic_dump_name.json")

