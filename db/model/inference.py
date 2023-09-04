from pydantic import BaseModel
from datetime import datetime
from .song import Song
from .playlist import Playlist
from .user import User
from .mixin.hash import HashableByIdMixin


class InferenceQuery(BaseModel):
    image_url: str
    genres: list[str]


class InferenceOutput(BaseModel):
    playlists: list[Playlist]
    songs: list[Song]


class InferenceFeedback(BaseModel):
    like_songs: list[Song]


class Inference(HashableByIdMixin, BaseModel):
    id: str
    user: User
    query: InferenceQuery
    output: InferenceOutput
    feedback: InferenceFeedback
    created_at: datetime
    updated_at: datetime
