from datetime import date

from db.repository import UserRepository, ArtistRepository, AlbumRepository, PlaylistRepository, SongRepository, AuthRepository, InferenceRepository
from db.model import User, Artist, Album, Playlist, Song, Auth, Inference


def create_user(user_repository: UserRepository) -> User:
    return user_repository.create_user()


def create_artist(artist_repository: ArtistRepository, genie_id: str = "A1", name: str = "주혜인") -> Artist:
    return artist_repository.create_artist(genie_id, name)


def create_album(
    album_repository: AlbumRepository,
    genie_id: str = "H1",
    name: str = "주혜아웃",
    img_url: str = "http://album.png",
    released_date: date = date(2000, 3, 15),
) -> Album:
    return album_repository.create_Album(genie_id, name, img_url, released_date)


def create_song(
    song_repository: SongRepository,
    album: Album,
    artist: Artist,
    genie_id: str = "S1",
    title: str = "노래",
    lyrics: str = "사가",
    like_cnt: int = 10,
    listener_cnt: int = 1,
    play_cnt: int = 2,
    genres: list[str] = ["락"],
    spotify_url: str = "http://song.mp4",
) -> Song:
    return song_repository.create_song(genie_id, title, lyrics, album, artist, like_cnt, listener_cnt, play_cnt, genres, spotify_url)


def create_playlist(
    playlist_repository: PlaylistRepository,
    songs: list[Song],
    genie_id: str = "P1",
    title: str = "주혜인의 플리",
    subtitle: str = "나 주혜인이 푸른 달이 뜨는 밤.. 방구석에서 몰래 듣는 노래를 모아봄",
    song_cnt: int = 1,
    like_cnt: int = 10,
    view_cnt: int = 20,
    tags: list[str] = ["tag"],
    img_url: str = "http://pl.png",
) -> Playlist:
    return playlist_repository.create_playlist(genie_id, title, subtitle, song_cnt, like_cnt, view_cnt, tags, songs, img_url)


def create_auth(auth_repository: AuthRepository, user: User, refresh_token: str) -> Auth:
    return auth_repository.create_auth(user=user, refresh_token=refresh_token)


def create_inference(
    inference_repository: InferenceRepository,
    user: User,
    output_playlists: list[Playlist],
    output_songs: list[Song],
    feedback_like_songs: list[Song],
    query_image_url: str = "http://123.com/123.png",
    query_genres: list[str] = ["POP"],
) -> Inference:
    return inference_repository.create_inference(
        user=user,
        output_playlists=output_playlists,
        output_songs=output_songs,
        feedback_like_songs=feedback_like_songs,
        query_image_url=query_image_url,
        query_genres=query_genres,
    )
