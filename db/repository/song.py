from ..document import SongDocument, ArtistDocument, AlbumDocument
from ..model import Album, Artist, Song
from ..exception import NotFoundSongException
from .common import find_album_doc_by_dto, find_artist_doc_by_dto
from .artist import ArtistRepository
from .album import AlbumRepository
from datetime import datetime
from mongoengine import QuerySet


class SongRepository:
    def create_song(
        self,
        genie_id: str,
        title: str,
        lyrics: str,
        album: Album,
        artist: Artist,
        like_cnt: int,
        listener_cnt: int,
        play_cnt: int,
        genres: list[str],
        spotify_url: str,
    ) -> Song:
        song = SongDocument(
            genie_id=genie_id,
            title=title,
            lyrics=lyrics,
            album=find_album_doc_by_dto(album),
            artist=find_artist_doc_by_dto(artist),
            like_cnt=like_cnt,
            listener_cnt=listener_cnt,
            play_cnt=play_cnt,
            genres=genres,
            spotify_url=spotify_url,
        )
        saved: SongDocument = song.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        song: SongDocument = SongDocument.objects(genie_id=genie_id).first()

        if not song:
            raise NotFoundSongException(f"Can't find song document: genie_id={genie_id}")

        song.delete()

    def find_by_genie_id(self, genie_id: str) -> Song | None:
        song: SongDocument = SongDocument.objects(genie_id=genie_id).first()

        if not song:
            return None

        return song.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Song]:
        songs: QuerySet[SongDocument] = SongDocument.objects(updated_at__gte=query_dt)

        if not songs:
            return None

        return [song.to_dto() for song in songs]

    def find_all(self) -> list[Song]:
        songs: QuerySet[SongDocument] = SongDocument.objects
        return [song.to_dto() for song in songs]

    @classmethod
    def _population_pipeline(cls) -> list[dict]:
        return [
            {
                "$lookup": {
                    "from": ArtistDocument._get_collection_name(),
                    "localField": "artist",
                    "foreignField": "_id",
                    "as": "artist",
                },
            },
            {
                "$lookup": {
                    "from": AlbumDocument._get_collection_name(),
                    "localField": "album",
                    "foreignField": "_id",
                    "as": "album",
                },
            },
        ]

    @classmethod
    def _song_dict2dto(cls, song_dict) -> Song:
        return Song(
            id=str(song_dict["_id"]),
            genie_id=song_dict["genie_id"],
            title=song_dict["title"],
            lyrics=song_dict["lyrics"],
            album=AlbumRepository._album_dict2dto(song_dict["album"][0]),
            artist=ArtistRepository._artist_dict2dto(song_dict["artist"][0]),
            like_cnt=song_dict["like_cnt"],
            listener_cnt=song_dict["listener_cnt"],
            play_cnt=song_dict["play_cnt"],
            genres=song_dict["genres"],
            spotify_url=song_dict.get("spotify_url", None),
            created_at=song_dict["created_at"],
            updated_at=song_dict["updated_at"],
        )
