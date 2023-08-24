import unittest

import db
from db.repository import AuthRepository, UserRepository
from db.exception import NotFoundAuthException
from .common import connect_to_db
from .document_provider import create_user, create_auth


class TestAuth(unittest.TestCase):
    auth_repository = AuthRepository()
    user_repository = UserRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_auth(self):
        user = create_user(self.user_repository)
        create_auth(self.auth_repository, user, "123")

    def test_find_by_refresh_token(self):
        user = create_user(self.user_repository)
        auth = create_auth(self.auth_repository, user, "123")

        found = self.auth_repository.find_by_refresh_token(auth.refresh_token)
        assert auth == found

    def test_delete_by_id(self):
        user = create_user(self.user_repository)
        auth = create_auth(self.auth_repository, user, "123")

        self.auth_repository.delete_by_id(auth.id)
        found = self.auth_repository.find_by_refresh_token(auth.refresh_token)
        assert found is None

        # not exists auth
        self.assertRaises(
            NotFoundAuthException,
            lambda: self.auth_repository.delete_by_id(auth.id),
        )
