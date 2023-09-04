from pydantic import BaseModel
from .mixin.hash import HashableByIdMixin


class User(HashableByIdMixin, BaseModel):
    id: str
