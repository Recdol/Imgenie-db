from .album import AlbumDocument
from .artist import ArtistDocument
from .playlist import PlaylistDocument
from .song import SongDocument
from .user import UserDocument
from .auth import AuthDocument
from .inference import InferenceDocument, InferenceQueryEmbeddedDocument, InferenceOutputEmbeddedDocument, InferenceFeedbackEmbeddedDocument

__all__ = [
    "AlbumDocument",
    "ArtistDocument",
    "PlaylistDocument",
    "SongDocument",
    "UserDocument",
    "AuthDocument",
    "InferenceDocument",
    "InferenceQueryEmbeddedDocument",
    "InferenceOutputEmbeddedDocument",
    "InferenceFeedbackEmbeddedDocument",
]
