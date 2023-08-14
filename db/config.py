from pydantic_settings import BaseSettings
from datetime import timedelta


class DBConfig(BaseSettings):
    auth_doc_exp_period: timedelta = timedelta(days=1)

    class Config:
        env_file = ".env"
