from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    app_name: str = "Anime Recomendation Engine"
    app_version: str = "0.0.1"

    database_host: str = "127.0.0.1"
    database_port: str = "6379"
    database_user: str = "postgre"
    database_password: str = "postgre"
    database_db: str = "postgre"

    class Meta:
        model_config = SettingsConfigDict(env_file=".env")
