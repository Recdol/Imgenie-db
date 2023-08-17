from ..document import PlaylistDocument, SongDocument
from ..exception import NotFoundPlaylistException
from ..model import Playlist, Song
from .common import find_song_docs_by_dto
from .song import SongRepository
from datetime import datetime
from mongoengine import QuerySet
from pymongo.command_cursor import CommandCursor


class PlaylistRepository:
    def create_playlist(
        self,
        genie_id: str,
        title: str,
        subtitle: str,
        song_cnt: int,
        like_cnt: int,
        view_cnt: int,
        tags: list[str],
        songs: list[Song],
        img_url: str,
    ) -> Playlist:
        song_docs = find_song_docs_by_dto(songs)
        playlist = PlaylistDocument(
            genie_id=genie_id,
            title=title,
            subtitle=subtitle,
            song_cnt=song_cnt,
            like_cnt=like_cnt,
            view_cnt=view_cnt,
            tags=tags,
            songs=song_docs,
            img_url=img_url,
        )
        saved: PlaylistDocument = playlist.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        playlist: PlaylistDocument = PlaylistDocument.objects(genie_id=genie_id).first()

        if not playlist:
            raise NotFoundPlaylistException(f"Can't find playlist document: genie_id={genie_id}")

        playlist.delete()

    def find_by_genie_id(self, genie_id: str) -> Playlist:
        pipeline = [{"$match": {"genie_id": genie_id}}, *self._population_pipeline()]

        result: CommandCursor = PlaylistDocument.objects.aggregate(*pipeline)

        if not result:
            return None

        playlist_dict = result.next()

        return self._playlist_dict2dto(playlist_dict=playlist_dict)

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Playlist]:
        playlists: QuerySet[PlaylistDocument] = PlaylistDocument.objects(updated_at__gte=query_dt)

        if not playlists:
            return None

        return [playlist.to_dto() for playlist in playlists]

    def find_all(self) -> list[Playlist]:
        playlists: QuerySet[PlaylistDocument] = PlaylistDocument.objects
        return [playlist.to_dto() for playlist in playlists]

    @classmethod
    def _population_pipeline(cls) -> list[dict]:
        return [
            {
                "$lookup": {
                    "from": SongDocument._get_collection_name(),
                    "localField": "songs",
                    "foreignField": "_id",
                    "as": "songs",
                    "pipeline": SongRepository._population_pipeline(),
                }
            },
        ]

    @classmethod
    def _playlist_dict2dto(cls, playlist_dict) -> Playlist:
        return Playlist(
            id=str(playlist_dict["_id"]),
            genie_id=playlist_dict["genie_id"],
            title=playlist_dict["title"],
            subtitle=playlist_dict["subtitle"],
            song_cnt=playlist_dict["song_cnt"],
            like_cnt=playlist_dict["like_cnt"],
            view_cnt=playlist_dict["view_cnt"],
            tags=playlist_dict["tags"],
            songs=[SongRepository._song_dict2dto(song_dict) for song_dict in playlist_dict["songs"]],
            img_url=playlist_dict["img_url"],
            created_at=playlist_dict["created_at"],
            updated_at=playlist_dict["updated_at"],
        )
