from src.models.group_nomenclature import GroupNomenclature
from src.models.ingredient import Ingredient
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.recipe import Recipe
from src.utils.deserializer import Deserializer


def test_recipe_deserialize():
    dict_recipe = {
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
            "Тестовый шаг",
        ],
        "uuid": "43801d89-2764-4b6b-989a-60718fdd9f2c"
    }
    test_recipe = Recipe.create(
        cooking_time_by_min=25,
        ingredients=[
            Ingredient.create(nomenclature=Nomenclature.create(
                group=GroupNomenclature.create(name="Молочные продукты"),
                name="Сливочное масло",
                range=Range.create(base_unit=None, conversion_factor=1.0,
                                   name="грамм")
            ),
                quantity=30
            )
        ],
        name="Панкейки с черникой",
        steps=["Тестовый шаг"],
    )
    deserializer = Deserializer()
    recipe_from_deserializer = deserializer.deserialize(Recipe, dict_recipe)
    assert recipe_from_deserializer == test_recipe
