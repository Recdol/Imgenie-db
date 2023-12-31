from mongoengine import Document, StringField, ReferenceField
from ..model import Auth
from ..config import config
from .user import UserDocument
from .mixin.date import CreatedAtMixin


class AuthDocument(CreatedAtMixin, Document):
    user = ReferenceField(UserDocument, required=True, unique=True)
    refresh_token = StringField(required=True)

    meta = {"indexes": [{"fields": ["created_at"], "expireAfterSeconds": int(config().auth_doc_exp_period.total_seconds())}]}

    def to_dto(self) -> Auth:
        return Auth(id=str(self.id), user=self.user.to_dto(), refresh_token=self.refresh_token, created_at=self.created_at)
