
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_name: str
    database_port: str
    database_host: str
    database_password: str
    database_username: str
    secret_key: str
    algorithm :str
    access_token_expiration_time: int
    refresh_token_expiration_days: int
    postgres_user:str | None = None
    postgres_password:str | None = None
    postgres_db:str | None = None

    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

settings= Settings()
