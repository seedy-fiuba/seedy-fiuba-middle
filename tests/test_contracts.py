import pytest
from src.main import app
from pytest_httpx import HTTPXMock
from httpx import AsyncClient
from .mocks import *

project_json = project_template.copy()
contract_json = contract_template.copy()

@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test"]


@pytest.mark.asyncio
async def test_get_contracts(httpx_mock: HTTPXMock):
    contract_response_mock = {
        'totalItems': 1,
        'contracts': [
            contract_json
        ],
        'totalPages': 1,
        'currentPage': 0
    }

    project_response_mock = {
        'size': 1,
        'results': [
            project_json
        ]
    }

    httpx_mock.add_response(method="GET",
                            url="https://seedy-fiuba-projects-api.herokuapp.com/api/contracts",
                            json=contract_response_mock)
    httpx_mock.add_response(method="GET",
                            url="https://seedy-fiuba-projects-api.herokuapp.com/api/project/search?id=1",
                            json=project_response_mock)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/contracts")

    print(response.text)
    assert response.status_code == 200
    assert response.json() == {
        'totalItems': 1,
        'results': [
            {
                'project': project_json,
                'contract': contract_json
            }
        ],
        'totalPages': 1,
        'currentPage': 0
    }
