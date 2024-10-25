import os.path

import pytest

from src.exceptions.custom import InvalidLengthException
from src.settings_manager import SettingsManager


def test_no_load_settings():
    """ Тест если ничего не загружать """
    settings_manager = SettingsManager()

    settings = settings_manager.settings
    assert settings.inn == 'Default value'
    assert settings.account == 'Default value'
    assert settings.correspondent_account == 'Default value'
    assert settings.bic == 'Default value'
    assert settings.name == 'Default value'
    assert settings.type_of_ownership == 'Default value'


# Тестовые данные
settings_dict = {
    "inn": "111111111111",
    "account": "22222222222",
    "correspondent_account": "33333333333",
    "bic": "444444444",
    "name": "555555555",
    "type_of_ownership": "66666"
}


def test_load_settings_from_dict():
    """ Тест загрузки данных из словаря """
    settings_manager = SettingsManager()
    settings_manager.from_dict(settings_dict)

    settings = settings_manager.settings
    assert settings.inn == "111111111111"
    assert settings.account == "22222222222"
    assert settings.correspondent_account == "33333333333"
    assert settings.bic == "444444444"
    assert settings.name == "555555555"
    assert settings.type_of_ownership == "66666"


def test_load_settings_from_json():
    """ Тест загрузки данных из json файла """
    settings_manager = SettingsManager()
    settings_manager.from_json(os.path.join(os.pardir, "settings.json"))

    settings = settings_manager.settings
    assert settings.inn == "123456789012"
    assert settings.account == "40702810123"
    assert settings.correspondent_account == "38104000000"
    assert settings.bic == "044525225"
    assert settings.name == "NeZorinEgor"
    assert settings.type_of_ownership == "SOLID"


def test_load_settings_from_another_dir_and_name():
    """ Тест загрузки данных из json файла """
    settings_manager = SettingsManager()
    settings_manager.from_json(os.path.join("file_for_test.json"))

    settings = settings_manager.settings
    assert settings.inn == "############"
    assert settings.account == "@@@@@@@@@@@"
    assert settings.correspondent_account == "!!!!!!!!!!!"
    assert settings.bic == "$$$$$$$$$"
    assert settings.name == "%%%%%%%%%%%%%%%%%%%%"
    assert settings.type_of_ownership == "^^^^^"


def test_invalid_fields_len():
    """ Тест на загрузку полей не корректной длинны """
    settings_manager = SettingsManager()

    with pytest.raises(InvalidLengthException, match="INN must be exactly 12 characters long, not 1"):
        settings_manager.from_dict({"inn": "1"})
    with pytest.raises(InvalidLengthException, match="ACCOUNT must be exactly 11 characters long, not 1"):
        settings_manager.from_dict({"account": "2"})
    with pytest.raises(InvalidLengthException, match="CORRESPONDENT_ACCOUNT must be exactly 11 characters long, not 1"):
        settings_manager.from_dict({"correspondent_account": "3"})
    with pytest.raises(InvalidLengthException, match="BIC must be exactly 9 characters long, not 1"):
        settings_manager.from_dict({"bic": "4"})
    with pytest.raises(InvalidLengthException, match="TYPE_OF_OWNERSHIP must be exactly 5 characters long, not 1"):
        settings_manager.from_dict({"type_of_ownership": "5"})


def test_is_singleton():
    """ Проверку на 1 экземпляр класса """
    settings_manager1 = SettingsManager()
    settings_manager1.from_dict(settings_dict)
    settings1 = settings_manager1.settings

    settings_manager2 = SettingsManager()
    settings_manager2.from_dict(settings_dict)
    settings2 = settings_manager2.settings
    assert settings1 is settings2
    assert settings_manager1 is settings_manager2
    assert settings1 == settings2
    assert settings_manager1 == settings_manager2
