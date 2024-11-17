from fastapi import HTTPException

from src.core.model import BaseModel
from src.core.observer import Observer, EventType


class DataStorage(Observer):
    def check_statement(self, event_type: EventType, entity: BaseModel):
        match event_type:
            case EventType.DELETE_NOMENCLATURE:
                # Пробегаемся по номенклатурам в рецептах
                for recipe in self.__data[DataStorage.recipe_id()]:
                    for ingredients in recipe.ingredients:
                        if ingredients.nomenclature == entity:
                            raise HTTPException(detail="Данная номенклатура есть в существующем рецепте.", status_code=409)

            case EventType.UPDATE_NOMENCLATURE:
                # Меняем номенклатуры в рецептах
                for recipe in self.__data[DataStorage.recipe_id()]:
                    for ingredients in recipe.ingredients:
                        if ingredients.nomenclature.uuid == entity.uuid:
                            ingredients.nomenclature = entity
                # Меняем номенклатуры в транзакциях
                for transaction in self.data[DataStorage.transaction_id()]:
                    if transaction.nomenclature.uuid == entity.uuid:
                        transaction.nomenclature = entity

    __data = {}
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DataStorage, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def data(self):
        return self.__data

    @staticmethod
    def group_id() -> str:
        return "group"

    @staticmethod
    def nomenclature_id() -> str:
        return "nomenclature"

    @staticmethod
    def range_id() -> str:
        return "range"

    @staticmethod
    def recipe_id() -> str:
        return "recipe"

    @staticmethod
    def transaction_id() -> str:
        return "transaction"


