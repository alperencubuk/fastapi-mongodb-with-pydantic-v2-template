from datetime import datetime
from test.conftest import database

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_boilerplate(client: AsyncClient):
    response = await client.post(
        "/boilerplate/",
        json={"email": "test_create@boilerplate.com"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test_create@boilerplate.com"


@pytest.mark.anyio
async def test_get_boilerplate(client: AsyncClient):
    boilerplate = {
        "email": "test_get@boilerplate.com",
        "create_date": datetime.utcnow(),
        "update_date": datetime.utcnow(),
    }
    new_boilerplate = await database["boilerplate"].insert_one(boilerplate)

    response = await client.get(f"/boilerplate/{new_boilerplate.inserted_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test_get@boilerplate.com"
