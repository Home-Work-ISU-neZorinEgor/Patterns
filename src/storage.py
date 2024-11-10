from src.core.observer import Observer, EventType


class DataStorage(Observer):
    def check_statement(self, event_type: EventType):
        if event_type == EventType.DELETE_NOMENCLATURE:
            pass
        elif event_type == EventType.UPDATE_NOMENCLATURE:
            pass

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


