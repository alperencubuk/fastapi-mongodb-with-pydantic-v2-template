from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "FastAPI MongoDB Template"
    VERSION: str = "2.0.0"

    API_KEY: str
    API_KEY_HEADER: str = "Authorization"

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_URI: str | None = None

    @model_validator(mode="after")
    def validator(self) -> "Settings":
        self.MONGO_URI = (
            f"mongodb://"
            f"{self.MONGO_INITDB_ROOT_USERNAME}:"
            f"{self.MONGO_INITDB_ROOT_PASSWORD}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}"
        )
        return self


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
