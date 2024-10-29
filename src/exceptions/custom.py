class InvalidTypeException(Exception):
    """
    Исключение, вызываемое при неверном типе данных.
    """
    pass


class InvalidLengthException(Exception):
    """
    Исключение, вызываемое при неверной длине данных.
    """
    pass


class UnsupportableReportFormatException(Exception):
    """
    Ошибка, вызываемая при неверно указанном формате в json файле
    """
    pass


class InvalidFieldException(Exception):
    """
    Ошибка, выбрасывающаяся, если при конвертации из словаря в модели нету такого поля
    """
    pass
