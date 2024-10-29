import datetime

from src.exceptions.proxy import ErrorProxy
from src.models.storehouse import Storehouse
from src.models.storehouse_transaction import TransactionType, StorehouseTransaction
from src.utils.validator import Validator
from src.storage import DataStorage
from src.models.group_nomenclature import GroupNomenclature
from src.models.ingredient import Ingredient
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.recipe import Recipe


class StartService:
    __repository: DataStorage
    __nomenclatures: dict = {}
    __error_proxy: ErrorProxy = ErrorProxy()

    def __init__(self, repository):
        Validator.validate(repository, DataStorage)
        self.__repository = repository

    def __create_groups(self):
        try:
            items = [
                GroupNomenclature.create(name="Бакалея"),
                GroupNomenclature.create(name="Молочные продукты"),
                GroupNomenclature.create(name="Яйца"),
                GroupNomenclature.create(name="Приправы"),
                GroupNomenclature.create(name="Ягода"),
            ]
            self.__repository.data[DataStorage.group_id()] = items
        except Exception as e:
            self.__error_proxy.error_message = str(e)

    def __create_range(self):
        try:
            gram = Range.create(name="грамм", conversion_factor=1.0)
            milliliter = Range.create(name="миллилитр", conversion_factor=1.0)
            piece = Range.create(name="шт.", conversion_factor=1.0)
            teaspoon = Range.create(name="чайная ложка", conversion_factor=1.0)
            tablespoon = Range.create(name="столовая ложка", conversion_factor=1.0)
            self.__repository.data[DataStorage.range_id()] = [gram, milliliter, piece, teaspoon, tablespoon]
        except Exception as e:
            self.__error_proxy.error_message = str(e)

    def __create_nomenclature(self):
        gram = self.__repository.data[DataStorage.range_id()][0]
        milliliter = self.__repository.data[DataStorage.range_id()][1]
        piece = self.__repository.data[DataStorage.range_id()][2]
        teaspoon = self.__repository.data[DataStorage.range_id()][3]

        group_grocery = [i for i in self.__repository.data[DataStorage.group_id()] if i.name == "Бакалея"][0]
        group_dairy = [i for i in self.__repository.data[DataStorage.group_id()] if i.name == "Молочные продукты"][0]
        group_eggs = [i for i in self.__repository.data[DataStorage.group_id()] if i.name == "Яйца"][0]
        group_berries = [i for i in self.__repository.data[DataStorage.group_id()] if i.name == "Ягода"][0]

        self.__nomenclatures["Пшеничная мука"] = Nomenclature.create(name="Пшеничная мука", group=group_grocery,
                                                                     range=gram)
        self.__nomenclatures["Молоко"] = Nomenclature.create(name="Молоко", group=group_dairy, range=milliliter)
        self.__nomenclatures["Яйцо"] = Nomenclature.create(name="Яйцо", group=group_eggs, range=piece)
        self.__nomenclatures["Сахар"] = Nomenclature.create(name="Сахар", group=group_grocery, range=gram)
        self.__nomenclatures["Разрыхлитель теста"] = Nomenclature.create(name="Разрыхлитель теста", group=group_grocery,
                                                                         range=gram)
        self.__nomenclatures["Соль"] = Nomenclature.create(name="Соль", group=group_grocery, range=teaspoon)
        self.__nomenclatures["Черника"] = Nomenclature.create(name="Черника", group=group_berries, range=gram)
        self.__nomenclatures["Сливочное масло"] = Nomenclature.create(name="Сливочное масло", group=group_dairy,
                                                                      range=gram)
        self.__repository.data[DataStorage.nomenclature_id()] = list(self.__nomenclatures.values())

    def __create_recipe(self):
        try:
            ingredients = [
                Ingredient.create(nomenclature=self.__nomenclatures["Пшеничная мука"], quantity=200),
                Ingredient.create(nomenclature=self.__nomenclatures["Молоко"], quantity=300),
                Ingredient.create(nomenclature=self.__nomenclatures["Яйцо"], quantity=2),
                Ingredient.create(nomenclature=self.__nomenclatures["Сахар"], quantity=50),
                Ingredient.create(nomenclature=self.__nomenclatures["Разрыхлитель теста"], quantity=10),
                Ingredient.create(nomenclature=self.__nomenclatures["Соль"], quantity=1),
                Ingredient.create(nomenclature=self.__nomenclatures["Черника"], quantity=150),
                Ingredient.create(nomenclature=self.__nomenclatures["Сливочное масло"], quantity=30)
            ]

            steps = [
                "Подготовьте все ингредиенты...",
                "Смешайте муку, сахар...",
                "Добавьте чернику в тесто...",
            ]

            cooking_time = 25

            recipe = Recipe.create(
                name="Панкейки с черникой",
                ingredients=ingredients,
                steps=steps,
                cooking_time_by_min=cooking_time
            )

            self.__repository.data[DataStorage.recipe_id()] = [recipe]
        except Exception as e:
            self.__error_proxy.error_message = str(e)

    def __create_transaction(self):
        storehouse = Storehouse.create(address="Иркутская обл., г. Шелехов, кв. 1, дом 1, квартира 1.")
        nomenclature = self.__repository.data[DataStorage.nomenclature_id()][0]
        transaction_type = TransactionType.INBOUND
        quantity = 1
        range = self.__repository.data[DataStorage.range_id()][0]
        time = datetime.datetime.now(datetime.timezone.utc)
        transaction = StorehouseTransaction.create(storehouse, nomenclature, transaction_type, quantity, range, time)
        self.__repository.data[DataStorage.transaction_id()] = [transaction]

    def create(self):
        self.__create_groups()
        self.__create_range()
        self.__create_nomenclature()
        self.__create_recipe()
        self.__create_transaction()

    @property
    def error_message(self) -> str:
        return self.__error_proxy.error_message

    @property
    def has_error(self) -> bool:
        return not self.__error_proxy.is_empty
