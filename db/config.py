from pydantic import BaseModel
from datetime import timedelta

__all__ = ["DEFAULT_AUTH_DOC_EXP_PERIOD", "setup_config", "config"]

DEFAULT_AUTH_DOC_EXP_PERIOD = timedelta(days=1)


class DBConfig(BaseModel):
    auth_doc_exp_period: timedelta = DEFAULT_AUTH_DOC_EXP_PERIOD


# It will be use db package-wide variable
# https://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
_config = DBConfig()


def setup_config(auth_doc_exp_period: timedelta):
    global _config

    _config.auth_doc_exp_period = auth_doc_exp_period


def config() -> DBConfig:
    return _config
