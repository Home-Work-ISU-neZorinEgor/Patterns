from src.models.group_nomenclature import GroupNomenclature
from src.models.ingredient import Ingredient
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.recipe import Recipe
from src.utils.validator import Validator


class Deserializer:
    @staticmethod
    def deserialize(cls, json: dict):
        Validator.validate(cls, type_=type)
        Validator.validate(json, type_=dict)

        return cls.from_dict(json)

    @staticmethod
    def from_dict(cls, json: dict):
        instance = cls()  # Создаем экземпляр класса

        # Обходим все атрибуты модели
        for key, value in json.items():
            if isinstance(value, dict):
                # Если значение - словарь, вызываем десериализацию для вложенного класса
                nested_cls = getattr(cls,
                                     key).get_class()  # Получаем класс для этого поля (предполагается, что он доступен)
                setattr(instance, key, Deserializer.deserialize(nested_cls, value))
            elif isinstance(value, list):
                # Если значение - список, обрабатываем каждый элемент
                item_cls = getattr(cls, key)[0].get_class()  # Предполагаем, что все элементы списка одного класса
                setattr(instance, key, [Deserializer.deserialize(item_cls, item) for item in value])
            else:
                setattr(instance, key, value)

        return instance
