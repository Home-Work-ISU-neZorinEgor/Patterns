import pydantic
from uuid import UUID, uuid4


class BaseModelDTO(pydantic.BaseModel):
    uuid: UUID = str(uuid4())
