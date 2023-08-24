from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    ListField,
    ReferenceField,
    EmbeddedDocumentField,
    ValidationError,
)
from ..model import Inference, InferenceOutput, InferenceQuery, InferenceFeedback
from .user import UserDocument
from .playlist import PlaylistDocument
from .song import SongDocument
from .mixin.date import CreatedAtMixin, UpdatedAtMixin


def _should_have_at_least_one_genre(genres: list[str]):
    if len(genres) <= 0:
        raise ValidationError("Inference should have at least one genere")


def _should_have_at_least_one_song(songs: list[SongDocument]):
    if len(songs) <= 0:
        raise ValidationError("Inference should have at least one song")


def _should_have_at_least_one_playlist(playlists: list[PlaylistDocument]):
    if len(playlists) <= 0:
        raise ValidationError("Inference should have at least one playlist")


def _feedback_like_songs_should_be_in_output_songs(feedback_like_songs: list[SongDocument], output_songs: list[SongDocument]):
    if not all(like_song in output_songs for like_song in feedback_like_songs):
        raise ValidationError("Inference Feedback songs should be in Inference Output songs")


class InferenceQueryEmbeddedDocument(EmbeddedDocument):
    image_url = StringField(required=True)
    genres = ListField(
        StringField(),
        required=True,
        validation=_should_have_at_least_one_genre,
    )

    def to_dto(self) -> InferenceQuery:
        return InferenceQuery(image_url=self.image_url, genres=self.genres)


class InferenceOutputEmbeddedDocument(EmbeddedDocument):
    playlists = ListField(ReferenceField(PlaylistDocument), required=True, validation=_should_have_at_least_one_playlist)
    songs = ListField(ReferenceField(SongDocument), required=True, validation=_should_have_at_least_one_song)

    def to_dto(self) -> InferenceOutput:
        return InferenceOutput(playlists=[playlist.to_dto() for playlist in self.playlists], songs=[song.to_dto() for song in self.songs])


class InferenceFeedbackEmbeddedDocument(EmbeddedDocument):
    like_songs = ListField(
        ReferenceField(SongDocument),
        required=True,
        validation=_should_have_at_least_one_genre,
    )

    def to_dto(self) -> InferenceFeedback:
        return InferenceFeedback(like_songs=[song.to_dto() for song in self.like_songs])


class InferenceDocument(CreatedAtMixin, UpdatedAtMixin, Document):
    user = ReferenceField(UserDocument, required=True)
    query = EmbeddedDocumentField(InferenceQueryEmbeddedDocument, required=True)
    output = EmbeddedDocumentField(InferenceOutputEmbeddedDocument, required=True)
    feedback = EmbeddedDocumentField(InferenceFeedbackEmbeddedDocument, required=True)

    def clean(self):
        _feedback_like_songs_should_be_in_output_songs(self.feedback.like_songs, self.output.songs)

    def to_dto(self) -> Inference:
        return Inference(
            id=str(self.id),
            user=self.user.to_dto(),
            query=self.query.to_dto(),
            output=self.output.to_dto(),
            feedback=self.feedback.to_dto(),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
