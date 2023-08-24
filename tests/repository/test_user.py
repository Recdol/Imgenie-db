import unittest

import db
from db.repository import UserRepository
from .common import connect_to_db
from .document_provider import create_user


class TestUser(unittest.TestCase):
    user_repository = UserRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_user(self):
        create_user(self.user_repository)

    def test_find_by_geine_id(self):
        user = create_user(self.user_repository)

        found = self.user_repository.find_by_id(user.id)
        assert user == found

    def test_find_all(self):
        users = [
            create_user(self.user_repository),
            create_user(self.user_repository),
            create_user(self.user_repository),
        ]

        found = self.user_repository.find_all()
        for user in users:
            assert user in found
