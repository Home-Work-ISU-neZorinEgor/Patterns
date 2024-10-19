from src.models.recipe import Recipe
from src.models.ingredient import Ingredient
from src.models.nomenclature import Nomenclature
from src.models.group_nomenclature import GroupNomenclature
from src.models.range import Range
from src.utils.validator import Validator


class Deserializer:
    @staticmethod
    def deserialize(cls, json: dict):
        Validator.validate(cls, type_=type)  # Убедимся, что передан класс
        Validator.validate(json, type_=dict)  # Убедимся, что передан словарь
        instance = cls()  # Создаем экземпляр класса
        # Проходим по полям класса и устанавливаем значения из json
        for key, value in json.items():
            # Проверяем наличие сеттера для атрибута (сеттеры обычно называются так же, как и поля)
            if hasattr(instance, key) and isinstance(getattr(cls, key, None), property):
                # Получаем тип атрибута из класса (по имени поля)
                attr_type = type(getattr(instance, key))

                # Если значение - это вложенный словарь, рекурсивно десериализуем его
                if isinstance(value, dict):
                    # Определяем тип вложенного объекта
                    nested_cls = Deserializer._get_nested_class(cls, key)
                    nested_value = Deserializer.deserialize(nested_cls, value)
                    setattr(instance, key, nested_value)

                # Если значение - это список, обрабатываем каждый элемент
                elif isinstance(value, list):
                    list_type = Deserializer._get_list_type(cls, key)
                    nested_list = [
                        Deserializer.deserialize(list_type, item) if isinstance(item, dict) else item
                        for item in value
                    ]
                    setattr(instance, key, nested_list)

                # Если значение простого типа (int, float, str), просто присваиваем
                else:
                    setattr(instance, key, value)

        return instance

    @staticmethod
    def _get_nested_class(cls, key: str):
        """
        Возвращает тип вложенного класса для поля, если это поле объект другого класса
        """
        # Здесь нужно прописать логику для определения типов полей по ключам.
        # Можно использовать аннотации типов или заранее подготовленную карту соответствий.
        field_mapping = {
            'nomenclature': Nomenclature,
            'group': GroupNomenclature,
            'range': Range,
            'ingredients': Ingredient
        }
        return field_mapping.get(key, None)

    @staticmethod
    def _get_list_type(cls, key: str):
        """
        Возвращает тип элементов списка для поля, если это список объектов
        """
        # Аналогичная логика для списков
        list_mapping = {
            'ingredients': Ingredient,
            'steps': str  # steps - это список строк
        }
        return list_mapping.get(key, None)


# Пример использования
recipe_dict = {
    "cooking_time_by_min": 25,
    "ingredients": [
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

deserializer = Deserializer()
recipe = deserializer.deserialize(Recipe, recipe_dict)
print(recipe.ingredients)
