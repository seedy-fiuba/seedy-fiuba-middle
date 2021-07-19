import pytest
from src.main import app
from pytest_httpx import HTTPXMock
from httpx import AsyncClient
from .mocks import *

user_json = user_template.copy()
balance_json = balance_template.copy()

@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test"]


@pytest.mark.asyncio
async def test_wallet_balance(httpx_mock: HTTPXMock):
    user_id = 10

    # Mock get user
    mock_get_user(httpx_mock, user_id, user_json)

    # Mock smart contract get balance
    mock_sc_get_balance(httpx_mock, user_json['walletPrivateKey'], balance_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/wallet/{user_id}")

    print(response.text)
    assert response.status_code == 200
    assert response.json() == balance_json


@pytest.mark.asyncio
async def test_wallet_transfer(httpx_mock: HTTPXMock):
    user_id = 10
    body = {
        'destinationAddress': '0x000',
        'amount': 0.001
    }

    # Mock get user
    mock_get_user(httpx_mock, user_id, user_json)

    # Mock smart contract get balance
    mock_sc_transfer_funds(httpx_mock,
                           {
                               'sourcePrivateKey': user_json['walletPrivateKey'],
                               'destinationAddress': body['destinationAddress'],
                               'amount': body['amount']
                           })

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/wallet/{user_id}/transfer", json=body)

    print(response.text)
    assert response.status_code == 204
    assert response.text == ''
