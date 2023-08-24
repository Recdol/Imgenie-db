import unittest

import db
from db.repository import InferenceRepository, UserRepository, PlaylistRepository, SongRepository, ArtistRepository, AlbumRepository
from .common import connect_to_db
from .document_provider import create_user, create_song, create_playlist, create_inference, create_album, create_artist


class TestUser(unittest.TestCase):
    inference_repository = InferenceRepository()
    user_repository = UserRepository()
    playlist_repository = PlaylistRepository()
    song_repository = SongRepository()
    artist_repository = ArtistRepository()
    album_repository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_inference(self):
        user = create_user(self.user_repository)

        album = create_album(self.album_repository)
        artist = create_artist(self.artist_repository)

        song = create_song(self.song_repository, album=album, artist=artist)
        playlist = create_playlist(self.playlist_repository, songs=[song])

        create_inference(self.inference_repository, user=user, output_playlists=[playlist], output_songs=[song], feedback_like_songs=[])

    def test_find_by_user(self):
        user = create_user(self.user_repository)

        album = create_album(self.album_repository)
        artist = create_artist(self.artist_repository)

        song = create_song(self.song_repository, album=album, artist=artist)
        playlist = create_playlist(self.playlist_repository, songs=[song])

        inference1 = create_inference(self.inference_repository, user=user, output_playlists=[playlist], output_songs=[song], feedback_like_songs=[])
        inference2 = create_inference(self.inference_repository, user=user, output_playlists=[playlist], output_songs=[song], feedback_like_songs=[])

        inferences = self.inference_repository.find_by_user(user)

        self.assertCountEqual(inferences, [inference1, inference2])

    def test_add_feedback_like_song_by_id(self):
        user = create_user(self.user_repository)

        album = create_album(self.album_repository)
        artist = create_artist(self.artist_repository)

        song = create_song(self.song_repository, album=album, artist=artist)
        playlist = create_playlist(self.playlist_repository, songs=[song])

        inference = create_inference(self.inference_repository, user=user, output_playlists=[playlist], output_songs=[song], feedback_like_songs=[])

        self.inference_repository.add_feedback_like_song_by_id(inference.id, song)

        inferences = self.inference_repository.find_by_user(user)

        self.assertIn(inference, inferences)

    def test_delete_feedback_like_song_by_id(self):
        user = create_user(self.user_repository)

        album = create_album(self.album_repository)
        artist = create_artist(self.artist_repository)

        song = create_song(self.song_repository, album=album, artist=artist)
        playlist = create_playlist(self.playlist_repository, songs=[song])

        inference = create_inference(self.inference_repository, user=user, output_playlists=[playlist], output_songs=[song], feedback_like_songs=[])

        self.inference_repository.add_feedback_like_song_by_id(inference.id, song)
        self.inference_repository.delete_feedback_like_song(inference.id, song)

        inferences = self.inference_repository.find_by_user(user)

        self.assertNotIn(inference, inferences)
