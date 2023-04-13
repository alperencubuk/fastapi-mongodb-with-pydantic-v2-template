from datetime import datetime

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase


@pytest.mark.asyncio
async def test_create_boilerplate(client: AsyncClient):
    payload = {
        "email": "test_create@boilerplate.com",
        "first_name": "boiler",
        "last_name": "plate",
    }
    response = await client.post("/boilerplate/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_get_boilerplate(client: AsyncClient, db: AsyncIOMotorDatabase):
    date = datetime.utcnow()
    payload = {
        "email": "test_get@boilerplate.com",
        "first_name": "boiler",
        "last_name": "plate",
        "create_date": date,
        "update_date": date,
    }
    new_boilerplate = await db["boilerplate"].insert_one(payload)
    response = await client.get(f"/boilerplate/{new_boilerplate.inserted_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
