import unittest
import time
from datetime import date, datetime, timedelta

import db
from db.repository import AlbumRepository
from db.exception import NotFoundAlbumException
from .common import connect_to_db
from .document_provider import create_album


class TestAlbum(unittest.TestCase):
    album_repository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_album(self):
        create_album(
            self.album_repository,
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

    def test_delete_by_genie_id(self):
        album = create_album(
            self.album_repository,
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

        self.album_repository.delete_by_genie_id(album.genie_id)
        found = self.album_repository.find_by_genie_id(album.genie_id)
        assert found is None

        # not exists playlist
        self.assertRaises(
            NotFoundAlbumException,
            lambda: self.album_repository.delete_by_genie_id(album.genie_id),
        )

    def test_find_by_geine_id(self):
        album = create_album(
            self.album_repository,
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

        found = self.album_repository.find_by_genie_id(album.genie_id)
        assert album == found

    def test_find_by_updated_at_gte(self):
        _album1 = create_album(  # noqa: F841
            self.album_repository,
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

        time.sleep(0.01)
        album2 = create_album(
            self.album_repository,
            "H2",
            "서민석",
            "http://album.png",
            date(2005, 12, 8),
        )

        found = self.album_repository.find_by_updated_at_gte(datetime.utcnow() - timedelta(milliseconds=1))
        assert [album2] == found

    def test_find_all(self):
        albums = [
            create_album(
                self.album_repository,
                "H1",
                "주혜인",
                "http://album.png",
                date(2001, 3, 13),
            ),
            create_album(
                self.album_repository,
                "H2",
                "서민석",
                "http://album.png",
                date(2005, 12, 8),
            ),
            create_album(
                self.album_repository,
                "H3",
                "이준영",
                "http://album.png",
                date(2000, 3, 15),
            ),
        ]

        found = self.album_repository.find_all()
        assert albums == found
