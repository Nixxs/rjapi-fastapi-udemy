import os

os.environ["ENV_STATE"] = "test"
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from rjapi.database import database, user_table
from rjapi.main import app


# only run once for all tests
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# provides the tests with the client object that can be used to make requests against
@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


# provides the database for our tests to use anc cleans it before each test
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


# allows tests to use the async client
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url=client.base_url,
    ) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details
