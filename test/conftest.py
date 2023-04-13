import asyncio

import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from source.core.database import get_db, mongo_client
from source.core.settings import settings
from source.main import app


def get_test_db() -> AsyncIOMotorDatabase:
    return mongo_client.test_database


app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={settings.API_KEY_HEADER: settings.API_KEY},
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def db():
    yield get_test_db()
    await mongo_client.drop_database("test_database")
