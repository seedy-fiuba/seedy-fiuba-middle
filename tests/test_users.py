import pytest
from src.main import app
from pytest_httpx import HTTPXMock
from httpx import AsyncClient
from .mocks import *

user_json = user_template.copy()

@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test"]


@pytest.mark.asyncio
async def test_get_user(httpx_mock: HTTPXMock):
    mock_get_user(httpx_mock, user_json['id'], user_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/users/{user_json['id']}")

    print('response: ' + response.text)
    assert response.status_code == 200
    assert response.json() == user_json


@pytest.mark.asyncio
async def test_put_user(httpx_mock: HTTPXMock):
    body = {
        'description': 'description'
    }
    mock_update_user(httpx_mock, user_json['id'], body, user_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/users/{user_json['id']}", json=body)

    print('response: ' + response.text)
    assert response.status_code == 200
    assert response.json() == user_json
