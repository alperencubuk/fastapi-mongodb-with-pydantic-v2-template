from functools import lru_cache

from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    APP_TITLE: str = "FastAPI MongoDB Template"
    VERSION: str = "1.0.0"

    API_KEY: str
    API_KEY_HEADER: str = "Authorization"

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_URI: str = None

    @root_validator
    def validator(cls, values) -> dict:
        values["MONGO_URI"] = (
            f"mongodb://"
            f'{values["MONGO_INITDB_ROOT_USERNAME"]}:'
            f'{values["MONGO_INITDB_ROOT_PASSWORD"]}@'
            f'{values["MONGO_HOST"]}:{values["MONGO_PORT"]}'
        )
        return values


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
