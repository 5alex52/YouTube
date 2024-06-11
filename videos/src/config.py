from typing import List
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["LOCAL", "DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: str

    @property
    def ASYNC_TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"

    @property
    def SYNC_TEST_DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    CORS_ORIGINS: List[str]
    CORS_HEADERS: List[str]
    CORS_METHODS: List[str]

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 5672

    RABBIT_HOST: str = "rabbit"
    RABBIT_PORT: int = 6379
    RABBIT_USER: str = "user"
    RABBIT_PASSWORD: str = "password"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings: Settings = Settings()
