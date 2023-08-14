from mongoengine import Document

from ..model import User
from .mixin.date import CreatedAtMixin, UpdatedAtMixin


class UserDocument(CreatedAtMixin, UpdatedAtMixin, Document):
    def to_dto(self) -> User:
        return User(id=str(self.id))
