from typing import Any, Type

from src.exceptions.custom import InvalidTypeException, InvalidLengthException, InvalidFieldException


class Validator:
    @staticmethod
    def validate(value: Any, type_: Type = None, len_: int = None):
        # Проверка типа данных, если тип указан
        if type_ is not None:
            if isinstance(type_, type):
                if not isinstance(value, type_):
                    raise InvalidTypeException(f"argument must be of type {type_.__name__}")

            # Если тип является списком, проверить тип элементов
            elif hasattr(type_, '__origin__') and type_.__origin__ is list:
                element_type = type_.__args__[0]
                if not isinstance(value, list):
                    raise InvalidTypeException(f"argument must be of type list[{element_type.__name__}]")
                for item in value:
                    if not isinstance(item, element_type):
                        raise InvalidTypeException(f"all elements must be of type {element_type.__name__}")

        # Проверка длины, если длина указана и значение поддерживает len()
        if len_ is not None and hasattr(value, '__len__') and len(value) != len_:
            raise InvalidLengthException(f"argument must have a length of {len_}, but got {len(value)}")

    @classmethod
    def check_fields(cls, data: dict, model: type):
        cls.validate(data, type_=dict)
        cls.validate(model, type_=type)

        attrs = dir(model)
        model_fields = [attr for attr in attrs if not attr.startswith('_') and not callable(getattr(model, attr))]
        for field in model_fields:
            if field not in data.keys():
                raise InvalidFieldException(f"Класс {model} не содержит property {field}")