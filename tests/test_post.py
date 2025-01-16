import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("this is the body", async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"
    response = await async_client.post("/post", json={"body": body})

    assert response.status_code == 201

    # check if the posted data is what we expected to see
    assert {"id": 0, "body": body}.items() <= response.json().items()
