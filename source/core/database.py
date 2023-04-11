from bson import ObjectId
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from source.core.settings import settings

mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)


def get_db() -> AsyncIOMotorDatabase:
    return mongo_client.database


database = get_db()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


async def create_index():
    await database["boilerplate"].create_index("email")


async def database_health() -> bool:
    try:
        await mongo_client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False
