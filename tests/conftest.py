from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from rjapi.main import app
from rjapi.routers.post import comment_table, post_table


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
    post_table.clear()
    comment_table.clear()
    yield


# allows tests to use the async client
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url=client.base_url,
    ) as ac:
        yield ac
