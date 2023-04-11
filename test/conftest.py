import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from source.core.database import get_db, mongo_client
from source.core.settings import settings
from source.main import app


def get_test_db() -> AsyncIOMotorDatabase:
    return mongo_client.test


database = get_test_db()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={settings.API_KEY_HEADER: settings.API_KEY},
    ) as client:
        yield client
    await mongo_client.drop_database("test")
