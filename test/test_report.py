import pytest

from src.core.report import FormatEnum
from src.models.ingredient import Ingredient
from src.models.range import Range, piece, gram, tablespoon
from src.models.recipe import Recipe
from src.report import ReportFactory


salad_recipe = Recipe(
    name="Греческий салат",
    ingredients=[
        Ingredient(name="Огурцы", unit=Range(name="piece", base_unit=piece, conversion_factor=2)),
        Ingredient(name="Помидоры", unit=Range(name="piece", base_unit=piece, conversion_factor=3)),
        Ingredient(name="Оливки", unit=Range(name="gram", base_unit=gram, conversion_factor=50)),
        Ingredient(name="Фета", unit=Range(name="gram", base_unit=gram, conversion_factor=100)),
        Ingredient(name="Оливковое масло", unit=Range(name="tablespoon", base_unit=tablespoon, conversion_factor=2)),
        Ingredient(name="Соль", unit=Range(name="taste", conversion_factor=1.0)),
        Ingredient(name="Перец", unit=Range(name="taste", conversion_factor=1.0)),
    ],
)

report_fabric = ReportFactory()


# Тест для CSV отчета
def test_csv_report():
    report = report_fabric.create(FormatEnum.CSV).create(salad_recipe)
    expected_header = "name;ingredients;lesson_topic"
    expected_data = "Греческий салат;[Ingredient(name=Огурцы, unit=piece (коэффициент пересчета: 2, базовая единица: piece)), Ingredient(name=Помидоры, unit=piece (коэффициент пересчета: 3, базовая единица: piece)), Ingredient(name=Оливки, unit=gram (коэффициент пересчета: 50, базовая единица: gram)), Ingredient(name=Фета, unit=gram (коэффициент пересчета: 100, базовая единица: gram)), Ingredient(name=Оливковое масло, unit=tablespoon (коэффициент пересчета: 2, базовая единица: tablespoon)), Ingredient(name=Соль, unit=taste (коэффициент пересчета: 1.0)), Ingredient(name=Перец, unit=taste (коэффициент пересчета: 1.0))];None"

    assert report.startswith(expected_header)
    assert expected_data in report


# Тест для Markdown отчета
def test_markdown_report():
    report = report_fabric.create(FormatEnum.MARKDOWN).create(salad_recipe)
    expected_report = (
        "# Греческий салат\n\n"
        "name | ingredients | lesson_topic\n"
        "--- | --- | ---\n"
        "Греческий салат | [Ingredient(name=Огурцы, unit=piece (коэффициент пересчета: 2, базовая единица: piece)), "
        "Ingredient(name=Помидоры, unit=piece (коэффициент пересчета: 3, базовая единица: piece)), "
        "Ingredient(name=Оливки, unit=gram (коэффициент пересчета: 50, базовая единица: gram)), "
        "Ingredient(name=Фета, unit=gram (коэффициент пересчета: 100, базовая единица: gram)), "
        "Ingredient(name=Оливковое масло, unit=tablespoon (коэффициент пересчета: 2, базовая единица: tablespoon)), "
        "Ingredient(name=Соль, unit=taste (коэффициент пересчета: 1.0)), "
        "Ingredient(name=Перец, unit=taste (коэффициент пересчета: 1.0))] | None\n"
    )

    assert report == expected_report


# Тест для JSON отчета
def test_json_report():
    report = report_fabric.create(FormatEnum.JSON).create(salad_recipe)
    expected_json = '''{
    "name": "Греческий салат",
    "ingredients": [
        "Ingredient(name=Огурцы, unit=piece (коэффициент пересчета: 2, базовая единица: piece))",
        "Ingredient(name=Помидоры, unit=piece (коэффициент пересчета: 3, базовая единица: piece))",
        "Ingredient(name=Оливки, unit=gram (коэффициент пересчета: 50, базовая единица: gram))",
        "Ingredient(name=Фета, unit=gram (коэффициент пересчета: 100, базовая единица: gram))",
        "Ingredient(name=Оливковое масло, unit=tablespoon (коэффициент пересчета: 2, базовая единица: tablespoon))",
        "Ingredient(name=Соль, unit=taste (коэффициент пересчета: 1.0))",
        "Ingredient(name=Перец, unit=taste (коэффициент пересчета: 1.0))"
    ],
    "lesson_topic": null
}'''
    assert report == expected_json




# Тест для RTF отчета
def test_rtf_report():
    report = report_fabric.create(FormatEnum.RTF).create(salad_recipe)
    expected_rtf = '''{\\rtf1\\ansi\n{\\b name\\cell ingredients\\cell lesson_topic \\row\nГреческий салат \\cell Ingredient(name=Огурцы, unit=piece (коэффициент пересчета: 2, базовая единица: piece)), Ingredient(name=Помидоры, unit=piece (коэффициент пересчета: 3, базовая единица: piece)), Ingredient(name=Оливки, unit=gram (коэффициент пересчета: 50, базовая единица: gram)), Ingredient(name=Фета, unit=gram (коэффициент пересчета: 100, базовая единица: gram)), Ingredient(name=Оливковое масло, unit=tablespoon (коэффициент пересчета: 2, базовая единица: tablespoon)), Ingredient(name=Соль, unit=taste (коэффициент пересчета: 1.0)), Ingredient(name=Перец, unit=taste (коэффициент пересчета: 1.0)) \\cell None \\cell \\row\n}\n}'''
    assert report == expected_rtf