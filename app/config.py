
from pydantic_settings import BaseSettings


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

    class Config:
        env_file=".env"

settings= Settings()
