from pydantic import BaseModel
from datetime import datetime
from .mixin.hash import HashableByIdMixin


class Artist(HashableByIdMixin, BaseModel):
    id: str
    genie_id: str
    name: str
    created_at: datetime
    updated_at: datetime
