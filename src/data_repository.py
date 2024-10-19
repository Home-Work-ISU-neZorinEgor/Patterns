class DataRepository:
    __data = {}
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DataRepository, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def data(self):
        return self.__data

    @staticmethod
    def group_id():
        return "group"

    @staticmethod
    def nomenclature_id():
        return "nomenclature"

    @staticmethod
    def range_id():
        return "range"

    @staticmethod
    def recipe_id():
        return "recipe"

    @staticmethod
    def transaction():
        return "transaction"
