from mongoengine import (
    Document,
    StringField,
    IntField,
    ListField,
    ReferenceField,
    ValidationError,
)
from ..model import Playlist
from .song import SongDocument
from .mixin.date import CreatedAtMixin, UpdatedAtMixin


def should_have_at_least_one_tag(tags: list[str]):
    if len(tags) <= 0:
        raise ValidationError("Playlist should have at least one tag")


def should_have_at_least_one_song(songs: list[SongDocument]):
    if len(songs) <= 0:
        raise ValidationError("Playlist should have at least one song")


class PlaylistDocument(CreatedAtMixin, UpdatedAtMixin, Document):
    genie_id = StringField(required=True)
    title = StringField(required=True)
    subtitle = StringField(required=True)
    song_cnt = IntField(required=True)
    like_cnt = IntField(required=True)
    view_cnt = IntField(required=True)
    tags = ListField(
        StringField(),
        required=True,
        validation=should_have_at_least_one_tag,
    )
    songs = ListField(
        ReferenceField(SongDocument),
        required=True,
        validation=should_have_at_least_one_song,
    )
    img_url = StringField(required=True)

    def to_dto(self) -> Playlist:
        return Playlist(
            id=str(self.id),
            genie_id=self.genie_id,
            title=self.title,
            subtitle=self.subtitle,
            song_cnt=self.song_cnt,
            like_cnt=self.like_cnt,
            view_cnt=self.view_cnt,
            tags=self.tags,
            songs=[song.to_dto() for song in self.songs],
            img_url=self.img_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
