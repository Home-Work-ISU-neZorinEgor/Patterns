from src.models.settings import Settings
from src.core.model import BaseModel


class Organization(BaseModel):
    """ Модель организации """

    def local_eq(self, other):
        return self.inn == other.inn

    __inn: str = ""
    __bic: str = ""
    __account: str = ""
    __type_of_ownership: str = ""

    def __init__(self, settings: Settings):
        self.__inn = settings.inn
        self.__bic = settings.bic
        self.__account = settings.account
        self.__type_of_ownership = settings.type_of_ownership

    def __str__(self):
        return f"inn: {self.__inn} \nbic: {self.__bic} \naccount: {self.__account} \ntype_of_ownership: {self.__type_of_ownership}"

    @property
    def inn(self):
        return self.__inn

    @property
    def bic(self):
        return self.__bic

    @property
    def account(self):
        return self.__account

    @property
    def type_of_ownership(self):
        return self.__type_of_ownership
