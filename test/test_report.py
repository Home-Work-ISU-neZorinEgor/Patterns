import datetime

import pytest
from src.models.storehouse_transaction import TransactionType
from src.storage import DataStorage
from src.service.starter import StartService


@pytest.fixture
def setup_service():
    # Создаем фикстуру для DataRepository
    repository = DataStorage()
    service = StartService(repository)
    return service, repository


def test_create_groups(setup_service):
    service, repository = setup_service
    service.create()
    # Проверяем, что группы созданы
    groups = repository.data[DataStorage.group_id()]
    assert len(groups) == 5 and len(groups) != 0


def test_create_ranges(setup_service):
    service, repository = setup_service
    service.create()

    # Проверяем, что диапазоны созданы
    ranges = repository.data[DataStorage.range_id()]
    assert len(ranges) == 5
    assert any(r.name == "грамм" for r in ranges)
    assert any(r.name == "миллилитр" for r in ranges)
    assert any(r.name == "шт." for r in ranges)
    assert any(r.name == "чайная ложка" for r in ranges)
    assert any(r.name == "столовая ложка" for r in ranges)


def test_create_nomenclature(setup_service):
    service, repository = setup_service
    service.create()

    # Проверяем, что номенклатуры созданы
    nomenclatures = repository.data[DataStorage.nomenclature_id()]
    assert len(nomenclatures) == 8
    assert any(n.name == "Пшеничная мука" for n in nomenclatures)
    assert any(n.name == "Молоко" for n in nomenclatures)
    assert any(n.name == "Яйцо" for n in nomenclatures)
    assert any(n.name == "Сахар" for n in nomenclatures)
    assert any(n.name == "Разрыхлитель теста" for n in nomenclatures)
    assert any(n.name == "Соль" for n in nomenclatures)
    assert any(n.name == "Черника" for n in nomenclatures)
    assert any(n.name == "Сливочное масло" for n in nomenclatures)


def test_create_recipe(setup_service):
    service, repository = setup_service
    service.create()

    # Проверяем, что рецепт создан
    recipes = repository.data[DataStorage.recipe_id()]
    assert len(recipes) == 1
    recipe = recipes[0]
    assert recipe.name == "Панкейки с черникой"
    assert len(recipe.ingredients) == 8
    assert len(recipe.steps) == 3
    assert recipe.cooking_time_by_min == 25


def test_create_transaction(setup_service):
    service, repository = setup_service
    service.create()

    # Проверяем, что транзакция создана
    transactions = repository.data[DataStorage.transaction_id()]
    assert len(transactions) == 1
    transaction = transactions[0]
    assert transaction.storehouse.address == "Иркутская обл., г. Шелехов, кв. 1, дом 1, квартира 1."
    assert transaction.nomenclature.name == "Пшеничная мука"
    assert transaction.quantity == 1
    assert transaction.transaction_type == TransactionType.INBOUND
    assert transaction.range.name == "грамм"
    assert isinstance(transaction.time, datetime.datetime)
