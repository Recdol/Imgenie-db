import unittest
import time
from datetime import date, datetime, timedelta

import db
from db.repository import AlbumRepository, SongRepository, ArtistRepository
from db.exception import (
    NotFoundAlbumException,
    NotFoundSongException,
    NotFoundArtistException,
)
from db.model import Album, Artist
from .document_provider import create_song, create_album, create_artist
from .common import connect_to_db


class TestSong(unittest.TestCase):
    song_repository = SongRepository()
    artist_repository = ArtistRepository()
    album_repository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_song(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        create_song(self.song_repository, artist=artist, album=album, genie_id="S1")

        # not exists artist
        fake_artist = Artist(
            id="123",
            genie_id="A3",
            name="없는것",
            created_at=date(2000, 3, 15),
            updated_at=date(2000, 3, 15),
        )
        fake_album = Album(
            id="456",
            genie_id="A9",
            name="없다",
            img_url="http://album.png",
            released_date=date(2000, 3, 15),
            created_at=date(2000, 3, 15),
            updated_at=date(2000, 3, 15),
        )
        self.assertRaises(
            NotFoundArtistException,
            lambda: create_song(
                self.song_repository, artist=fake_artist, album=album, genie_id="S2"
            ),
        )
        self.assertRaises(
            NotFoundAlbumException,
            lambda: create_song(
                self.song_repository, artist=artist, album=fake_album, genie_id="E1"
            ),
        )

    def test_delete_by_genie_id(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)

        self.song_repository.delete_by_genie_id(song.genie_id)
        found = self.song_repository.find_by_genie_id(song.genie_id)
        assert found is None

        # not exists song
        self.assertRaises(
            NotFoundSongException,
            lambda: self.song_repository.delete_by_genie_id(song.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)

        found = self.song_repository.find_by_genie_id(song.genie_id)
        assert song == found

    def test_find_by_id(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)

        found = self.song_repository.find_by_id(song.id)
        assert song == found

    def test_find_by_updated_at_gte(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)

        song1 = create_song(
            self.song_repository, artist=artist, album=album, genie_id="S1"
        )  # noqa: F841
        time.sleep(0.01)
        song2 = create_song(
            self.song_repository, artist=artist, album=album, genie_id="S2"
        )

        found = self.song_repository.find_by_updated_at_gte(
            datetime.utcnow() - timedelta(milliseconds=1)
        )
        assert [song2] == found

    def test_find_all(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        songs = [
            create_song(
                self.song_repository, artist=artist, album=album, genie_id="S1"
            ),
            create_song(
                self.song_repository, artist=artist, album=album, genie_id="S2"
            ),
            create_song(
                self.song_repository, artist=artist, album=album, genie_id="S3"
            ),
        ]

        found = self.song_repository.find_all()
        assert songs == found
