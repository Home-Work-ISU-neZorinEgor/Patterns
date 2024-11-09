from pydantic import BaseModel


class TransactionTypeDto(BaseModel):
    name: str
    value: int
