from typing import Any

from bson import ObjectId
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from pymongo.errors import ConnectionFailure

from source.core.settings import settings

mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)


def get_db() -> AsyncIOMotorDatabase:
    return mongo_client.database


database = get_db()


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


async def create_index():
    await database["boilerplate"].create_index("email")


async def database_health() -> bool:
    try:
        await mongo_client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False
