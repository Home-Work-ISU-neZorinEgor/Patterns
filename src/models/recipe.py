from typing import List
from src.core.model import BaseModel
from src.utils.validator import Validator
from src.models.ingredient import Ingredient
import datetime


class Recipe(BaseModel):
    __name: str = None
    __ingredients: List[Ingredient] = None   # Список объектов Ingredient
    __steps: List[str] = None
    __cooking_time_by_min: float | int = None
    __time: datetime.datetime = None

    def local_eq(self, other):
        return self.name == other.name and self.ingredients == other.ingredients

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj.name = data['name']
        obj.cooking_time_by_min = data['cooking_time_by_min']
        obj.ingredients = [Ingredient.from_dict(ingredient) for ingredient in data['ingredients']]
        obj.steps = data['steps']
        obj.time = datetime.datetime.fromtimestamp(data['time'])
        obj.uuid = data['uuid']
        return obj

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate(value, type_=str)
        self.__name = value

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: List[Ingredient]):
        Validator.validate(value, type_=List[Ingredient])
        self.__ingredients = value

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value: List[str]):
        Validator.validate(value, type_=List[str])
        self.__steps = value

    @property
    def cooking_time_by_min(self):
        return self.__cooking_time_by_min

    @cooking_time_by_min.setter
    def cooking_time_by_min(self, value: float | int):
        Validator.validate(value, type_=int | float)
        self.__cooking_time_by_min = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, new_time):
        self.__time = new_time

    @staticmethod
    def create(name: str, ingredients: List[Ingredient], steps: List[str], cooking_time_by_min: float | int, time):
        recipe = Recipe()
        recipe.name = name
        recipe.ingredients = ingredients
        recipe.steps = steps
        recipe.cooking_time_by_min = cooking_time_by_min
        recipe.time = time
        return recipe

    def __str__(self):
        ingredients_str = ', '.join([str(ingredient) for ingredient in self.ingredients])  # Используем геттер
        steps_str = '\n'.join([f"{idx + 1}. {step}" for idx, step in enumerate(self.steps)])  # Используем геттер
        return (
            f"Recipe: {self.name}\n"  # Используем геттер
            f"Ingredients: {ingredients_str}\n"
            f"Steps:\n{steps_str}\n"
            f"Cooking time: {self.cooking_time_by_min} minutes\n"  # Используем геттер
            f"Creation time: {self.time}\n"  # Используем геттер
        )
