import os

from src.data_repository import DataRepository
from src.models.recipe import Recipe
from src.settings_manager import SettingsManager
from src.start_service import StartService
from src.utils.validator import Validator


class Deserializer:
    @staticmethod
    def _is_primitive(value):
        return isinstance(value, (int, float, bool, str, bytes, type(None)))

    @staticmethod
    def deserialize(cls, json: dict):
        Validator.validate(cls, type_=type)  # Убедимся, что передан класс
        instance = cls()  # Создаем новый экземпляр класса

        for key, value in json.items():
            if key == "uuid":
                continue

            # Если это примитив и он есть у класса
            if hasattr(instance, key) and Deserializer._is_primitive(value):
                setattr(instance, key, value)
            # Если это кастомная модель и она есть в классе
            elif hasattr(instance, key) and isinstance(value, dict):
                dict_fields = value.keys()
                model_fields = filter(lambda x: not x.startswith("_") and not callable(getattr(cls, x)), dir(cls))
                if set(dict_fields) == set(model_fields):
                    # Рекурсивно десериализуем значение в новый экземпляр класса
                    sub_instance = Deserializer.deserialize(cls, value)
                    setattr(instance, key, sub_instance)

        return instance


recipe_dict = {
    "cooking_time_by_min": 25,
    "ingredients": [
        {
            "nomenclature": {
                "group": {
                    "name": "Бакалея",
                    "uuid": "954e93a9-5dd8-4866-9d67-0a77732ddd7c"
                },
                "name": "Пшеничная мука",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "грамм",
                    "uuid": "d2fcb3db-13fa-4986-b6ee-6ce33aff3d86"
                },
                "uuid": "81b03880-709d-401c-8053-8453c1e2dbf5"
            },
            "quantity": 200,
            "uuid": "0a547f7f-cacd-42e7-87ee-c8d4ad46cd22"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Молочные продукты",
                    "uuid": "6eafec95-1f0e-4278-931d-e353560b6c74"
                },
                "name": "Молоко",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "миллилитр",
                    "uuid": "e7889a25-3b93-4f80-ad8a-54fb3412a197"
                },
                "uuid": "0dc6e051-5014-4b52-91c1-ab09868683d8"
            },
            "quantity": 300,
            "uuid": "1d024795-0239-4f98-a7bd-0a2ce797f580"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Яйца",
                    "uuid": "0e2b245e-3654-434f-8702-e4484ecaf094"
                },
                "name": "Яйцо",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "шт.",
                    "uuid": "580cbeaa-a658-4dd2-a1b9-8264a44631e9"
                },
                "uuid": "410f1350-45bb-448c-8600-fc0241955c34"
            },
            "quantity": 2,
            "uuid": "11e8b8aa-6f20-4bb0-91be-4b757deb837d"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Бакалея",
                    "uuid": "954e93a9-5dd8-4866-9d67-0a77732ddd7c"
                },
                "name": "Сахар",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "грамм",
                    "uuid": "d2fcb3db-13fa-4986-b6ee-6ce33aff3d86"
                },
                "uuid": "c628b4e7-b4ec-41bc-9a2a-76e70bba7894"
            },
            "quantity": 50,
            "uuid": "71c73e20-fc20-434a-b91f-a6dd14d90235"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Бакалея",
                    "uuid": "954e93a9-5dd8-4866-9d67-0a77732ddd7c"
                },
                "name": "Разрыхлитель теста",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "грамм",
                    "uuid": "d2fcb3db-13fa-4986-b6ee-6ce33aff3d86"
                },
                "uuid": "757a29d8-6ca6-4c3b-9d9d-bbcc5673dae9"
            },
            "quantity": 10,
            "uuid": "ffd26475-e18f-4de5-be27-92e88137f9a0"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Бакалея",
                    "uuid": "954e93a9-5dd8-4866-9d67-0a77732ddd7c"
                },
                "name": "Соль",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "чайная ложка",
                    "uuid": "674df8d9-ab93-474d-a914-ab781abbc1a7"
                },
                "uuid": "83b2802a-5a20-4b71-8a94-75c4af98e524"
            },
            "quantity": 0.5,
            "uuid": "83806379-69d8-4adc-afd5-de14c80378c9"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Ягода",
                    "uuid": "961b4fb8-fde0-4f86-ae33-57795f4a3ede"
                },
                "name": "Черника",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "грамм",
                    "uuid": "d2fcb3db-13fa-4986-b6ee-6ce33aff3d86"
                },
                "uuid": "029ba567-f0c8-4b48-b6ba-630e079b86cc"
            },
            "quantity": 150,
            "uuid": "9af2540f-1c1f-46b0-9a86-760655ad93e6"
        },
        {
            "nomenclature": {
                "group": {
                    "name": "Молочные продукты",
                    "uuid": "6eafec95-1f0e-4278-931d-e353560b6c74"
                },
                "name": "Сливочное масло",
                "range": {
                    "base_unit": None,
                    "conversion_factor": 1.0,
                    "name": "грамм",
                    "uuid": "d2fcb3db-13fa-4986-b6ee-6ce33aff3d86"
                },
                "uuid": "d4c36c8d-fe56-4d9e-8cdc-8cd009c6b5f8"
            },
            "quantity": 30,
            "uuid": "5f262279-a57b-4335-bb25-88a2c1ed458b"
        }
    ],
    "name": "Панкейки с черникой",
    "steps": [
        "Подготовьте все ингредиенты. В глубокой миске смешайте муку, сахар, разрыхлитель и соль.",
        "В отдельной миске взбейте яйца и добавьте молоко. Хорошо перемешайте.",
        "Влейте яичную смесь в сухие ингредиенты и перемешайте до однородности. Постарайтесь не перебить тесто, небольшие комочки допустимы.",
        "В растопленное сливочное масло добавьте тесто и аккуратно перемешайте.",
        "Добавьте чернику в тесто и осторожно перемешайте, чтобы не повредить ягоды.",
        "Разогрейте сковороду на среднем огне и слегка смажьте ее маслом.",
        "Вылейте половник теста на сковороду. Готовьте до появления пузырьков на поверхности, затем переверните и жарьте до золотистого цвета.",
        "Повторяйте процесс, пока не израсходуете все тесто.",
        "Подавайте панкейки горячими, можно с медом или кленовым сиропом."
    ],
    "time": 1727968784.338826,
    "uuid": "43801d89-2764-4b6b-989a-60718fdd9f2c"
}

