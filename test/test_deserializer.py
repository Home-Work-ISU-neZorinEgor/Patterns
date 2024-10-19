from src.models.range import Range
from src.utils.deserializer import Deserializer


def test_deserialize_range():
    # Ожидаемый объект Range для сравнения
    expected_range = Range.create(name="кг.", conversion_factor=1000,
                                  base_unit=Range.create(name="гр.", conversion_factor=1, base_unit=None))

    range_dict = {
        "uuid": "65256fbf-ca34-4636-95f2-87615dc98648",
        "name": "кг.",
        "conversion_factor": 1000,
        "base_unit": {
            "uuid": "7f2d6b74-0d7f-46e8-8f94-5d3c75929e1b",
            "name": "гр.",
            "conversion_factor": 1,
            "base_unit": None
        }
    }

    deserialized_range = Deserializer.deserialize(Range, range_dict)

    # Проверка основных свойств
    assert deserialized_range.name == expected_range.name, "Название не совпадает"
    assert deserialized_range.conversion_factor == expected_range.conversion_factor, "Коэффициент конверсии не совпадает"

    # Проверка base_unit
    assert deserialized_range.base_unit is not None, "base_unit должен быть не None"
    assert deserialized_range.base_unit.name == expected_range.base_unit.name, "Название base_unit не совпадает"
    assert deserialized_range.base_unit.conversion_factor == expected_range.base_unit.conversion_factor, "Коэффициент конверсии base_unit не совпадает"

    # Проверка корректности полного сравнения объектов
    assert deserialized_range == expected_range, "Объекты Range не совпадают"

    # Дополнительная проверка вложенности base_unit
    assert deserialized_range.base_unit.base_unit is None, "Вложенный base_unit должен быть None"
