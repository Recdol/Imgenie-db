from .album import NotFoundAlbumException
from .artist import NotFoundArtistException
from .playlist import NotFoundPlaylistException
from .song import NotFoundSongException
from .user import NotFoundUserException
from .auth import NotFoundAuthException

__all__ = [
    "NotFoundAlbumException",
    "NotFoundArtistException",
    "NotFoundPlaylistException",
    "NotFoundSongException",
    "NotFoundUserException",
    "NotFoundAuthException",
]
