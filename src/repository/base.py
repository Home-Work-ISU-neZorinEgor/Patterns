from abc import ABC


class ABCRepository(ABC):
    __data = {}
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ABCRepository, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @staticmethod
    def group_key():
        return "group"

    @property
    def data(self):
        return self.__data
