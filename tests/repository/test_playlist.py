import unittest
import time
from datetime import date, datetime, timedelta

import db
from db.repository import PlaylistRepository, SongRepository, ArtistRepository, AlbumRepository
from db.exception import (
    NotFoundPlaylistException,
    NotFoundSongException,
)
from db.model import Song
from .common import connect_to_db
from .document_provider import create_artist, create_album, create_song, create_playlist


class TestPlaylist(unittest.TestCase):
    song_repository = SongRepository()
    playlist_repository = PlaylistRepository()
    artist_repository = ArtistRepository()
    album_repository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_playlist(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album, genie_id="S1")
        create_playlist(self.playlist_repository, songs=[song], genie_id="1")

        # not exists song
        fake_song = Song(
            id="1234",
            genie_id="S3",
            title="title",
            lyrics="lyrics",
            album=album,
            artist=artist,
            like_cnt=10,
            listener_cnt=1,
            play_cnt=1,
            genres=["genres"],
            created_at=date(2000, 3, 15),
            updated_at=date(2000, 3, 15),
            spotify_url=None,
        )
        self.assertRaises(NotFoundSongException, lambda: create_playlist(self.playlist_repository, songs=[fake_song], genie_id="2"))

    def test_delete_by_genie_id(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)
        playlist = create_playlist(self.playlist_repository, songs=[song])

        self.playlist_repository.delete_by_genie_id(playlist.genie_id)
        found = self.playlist_repository.find_by_genie_id(playlist.genie_id)
        assert found is None

        # not exists playlist
        self.assertRaises(
            NotFoundPlaylistException,
            lambda: self.playlist_repository.delete_by_genie_id(playlist.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)
        playlist = create_playlist(self.playlist_repository, songs=[song])

        found = self.playlist_repository.find_by_genie_id(playlist.genie_id)
        assert playlist == found

    def test_find_by_updated_at_gte(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)

        playlist1 = create_playlist(self.playlist_repository, songs=[song], genie_id="P1")  # noqa: F841
        time.sleep(0.01)
        playlist2 = create_playlist(self.playlist_repository, songs=[song], genie_id="P2")

        found = self.playlist_repository.find_by_updated_at_gte(datetime.utcnow() - timedelta(milliseconds=1))
        assert [playlist2] == found

    def test_find_all(self):
        artist = create_artist(self.artist_repository)
        album = create_album(self.album_repository)
        song = create_song(self.song_repository, artist=artist, album=album)

        playlists = [
            create_playlist(self.playlist_repository, songs=[song], genie_id="P1"),
            create_playlist(self.playlist_repository, songs=[song], genie_id="P2"),
            create_playlist(self.playlist_repository, songs=[song], genie_id="P3"),
        ]

        found = self.playlist_repository.find_all()
        assert playlists == found
