from pydantic import BaseModel
from datetime import date, datetime
from .mixin.hash import HashableByIdMixin


class Album(HashableByIdMixin, BaseModel):
    id: str
    genie_id: str
    name: str
    img_url: str
    released_date: date
    created_at: datetime
    updated_at: datetime
