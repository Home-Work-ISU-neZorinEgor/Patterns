from src.errors.proxy import ErrorProxy
from src.utils.validator import Validator
from src.data_repository import DataRepository
from src.models.group_nomenclature import GroupNomenclature
from src.models.ingredient import Ingredient
from src.models.nomenclature import Nomenclature
from src.models.range import Range
from src.models.recipe import Recipe


class StartService:
    __repository: DataRepository
    __nomenclatures: dict = {}
    __error_proxy: ErrorProxy = ErrorProxy()

    def __init__(self, repository):
        Validator.validate(repository, DataRepository)
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
            self.__repository.data[DataRepository.group_id()] = items
        except Exception as e:
            self.__error_proxy.error_message = str(e)  # Установка сообщения об ошибке

    def __create_range(self):
        try:
            gram = Range.create(name="грамм", conversion_factor=1.0)
            milliliter = Range.create(name="миллилитр", conversion_factor=1.0)
            piece = Range.create(name="шт.", conversion_factor=1.0)
            teaspoon = Range.create(name="чайная ложка", conversion_factor=1.0)
            tablespoon = Range.create(name="столовая ложка", conversion_factor=1.0)
            self.__repository.data[DataRepository.range_id()] = [gram, milliliter, piece, teaspoon, tablespoon]
        except Exception as e:
            self.__error_proxy.error_message = str(e)

    def __create_nomenclature(self):
        try:
            gram = self.__repository.data[DataRepository.range_id()][0]
            milliliter = self.__repository.data[DataRepository.range_id()][1]
            piece = self.__repository.data[DataRepository.range_id()][2]
            teaspoon = self.__repository.data[DataRepository.range_id()][3]

            group_grocery = [i for i in self.__repository.data[DataRepository.group_id()] if i.name == "Бакалея"][0]
            group_dairy = [i for i in self.__repository.data[DataRepository.group_id()] if i.name == "Молочные продукты"][0]
            group_eggs = [i for i in self.__repository.data[DataRepository.group_id()] if i.name == "Яйца"][0]
            group_berries = [i for i in self.__repository.data[DataRepository.group_id()] if i.name == "Ягода"][0]

            self.__nomenclatures["Пшеничная мука"] = Nomenclature.create(name="Пшеничная мука", group=group_grocery, range=gram)
            self.__nomenclatures["Молоко"] = Nomenclature.create(name="Молоко", group=group_dairy, range=milliliter)
            self.__nomenclatures["Яйцо"] = Nomenclature.create(name="Яйцо", group=group_eggs, range=piece)
            self.__nomenclatures["Сахар"] = Nomenclature.create(name="Сахар", group=group_grocery, range=gram)
            self.__nomenclatures["Разрыхлитель теста"] = Nomenclature.create(name="Разрыхлитель теста", group=group_grocery, range=gram)
            self.__nomenclatures["Соль"] = Nomenclature.create(name="Соль", group=group_grocery, range=teaspoon)
            self.__nomenclatures["Черника"] = Nomenclature.create(name="Черника", group=group_berries, range=gram)
            self.__nomenclatures["Сливочное масло"] = Nomenclature.create(name="Сливочное масло", group=group_dairy, range=gram)

            self.__repository.data[DataRepository.nomenclature_id()] = list(self.__nomenclatures.values())
        except Exception as e:
            self.__error_proxy.error_message = str(e)

    def __create_recipe(self):
        try:
            ingredients = [
                Ingredient(nomenclature=self.__nomenclatures["Пшеничная мука"], quantity=200),  # 200 гр
                Ingredient(nomenclature=self.__nomenclatures["Молоко"], quantity=300),  # 300 мл
                Ingredient(nomenclature=self.__nomenclatures["Яйцо"], quantity=2),  # 2 шт
                Ingredient(nomenclature=self.__nomenclatures["Сахар"], quantity=50),  # 50 гр
                Ingredient(nomenclature=self.__nomenclatures["Разрыхлитель теста"], quantity=10),  # 10 гр
                Ingredient(nomenclature=self.__nomenclatures["Соль"], quantity=0.5),  # 1/2 ч.л. (0.5 ч.л.)
                Ingredient(nomenclature=self.__nomenclatures["Черника"], quantity=150),  # 150 гр
                Ingredient(nomenclature=self.__nomenclatures["Сливочное масло"], quantity=30)  # 30 гр
            ]

            steps = [
                "Подготовьте все ингредиенты. В глубокой миске смешайте муку, сахар, разрыхлитель и соль.",
                "В отдельной миске взбейте яйца и добавьте молоко. Хорошо перемешайте.",
                "Влейте яичную смесь в сухие ингредиенты и перемешайте до однородности. Постарайтесь не перебить тесто, небольшие комочки допустимы.",
                "В растопленное сливочное масло добавьте тесто и аккуратно перемешайте.",
                "Добавьте чернику в тесто и осторожно перемешайте, чтобы не повредить ягоды.",
                "Разогрейте сковороду на среднем огне и слегка смажьте ее маслом.",
                "Вылейте половник теста на сковороду. Готовьте до появления пузырьков на поверхности, затем переверните и жарьте до золотистого цвета.",
                "Повторяйте процесс, пока не израсходуете все тесто.",
                "Подавайте панкейки горячими, можно с медом или кленовым сиропом."
            ]

            cooking_time = 25  # Время приготовления в минутах

            recipe = Recipe.create(
                name="Панкейки с черникой",
                ingredients=ingredients,  # Используем список ингредиентов
                steps=steps,
                cooking_time_by_min=cooking_time
            )

            self.__repository.data[DataRepository.recipe_id()] = [recipe]
        except Exception as e:
            self.__error_proxy.error_message = str(e)

    def create(self):
        self.__create_groups()
        self.__create_range()
        self.__create_nomenclature()
        self.__create_recipe()

    @property
    def error_message(self) -> str:
        return self.__error_proxy.error_message

    @property
    def has_error(self) -> bool:
        return not self.__error_proxy.is_empty
