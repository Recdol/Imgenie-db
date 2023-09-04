from pydantic import BaseModel
from .user import User
from datetime import datetime
from .mixin.hash import HashableByIdMixin


class Auth(HashableByIdMixin, BaseModel):
    id: str
    user: User
    refresh_token: str
    created_at: datetime
