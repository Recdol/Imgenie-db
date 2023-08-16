import mongoengine
from . import model
from . import repository
from . import exception
from . import config as _config

from .model import *  # noqa: F401
from .repository import *  # noqa: F401
from .exception import *  # noqa: F401
from .config import *  # noqa: F401


def connect(db: str, host: str, username: str, password: str, mongo_client_class=None):
    mongoengine.connect(
        db,
        host=host,
        username=username,
        password=password,
        mongo_client_class=mongo_client_class,
    )


def disconnect():
    mongoengine.disconnect()


__all__ = model.__all__ + exception.__all__ + repository.__all__ + _config.__all__ + ["connect", "disconnect"]
