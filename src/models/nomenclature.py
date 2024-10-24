from src.core.model import BaseModel
from src.utils.validator import Validator
from src.models.group_nomenclature import GroupNomenclature
from src.models.range import Range


class Nomenclature(BaseModel):
    __name: str = None
    __group: GroupNomenclature = None
    __range: Range = None

    def local_eq(self, other):
        return self.name == other.name

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj.name = data['name']
        obj.group = GroupNomenclature.from_dict(data['group'])
        obj.range = Range.from_dict(data['range'])
        obj.uuid = data['uuid']
        return obj

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, new_group) -> None:
        self.__group = new_group

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, new_range):
        self.__range = new_range

    @staticmethod
    def create(name, group, range):
        Validator.validate(name, type_=str)
        Validator.validate(group, type_=GroupNomenclature)
        Validator.validate(range, type_=Range)
        item = Nomenclature()
        item.name = name
        item.group = group
        item.range = range
        return item

    def __str__(self):
        group_str = str(self.__group) if self.__group else "Нету группы"
        return f"Продукт: {self.__name}, Группа: {group_str}, Единица: {self.__range}"

    def __hash__(self):
        """
        Хэшируем по имени, группе и единице измерения
        """
        return hash((self.name, self.group, self.range))