import pytest
from fastapi.testclient import TestClient
from src.main import app
from pytest_httpx import HTTPXMock
from httpx import AsyncClient

client = TestClient(app)

review_json = {
    'reviewerId': 0,
    'projectId': 1,
    'id': 0,
    'status': 'pending',
    'createdAt': '',
    'updatedAt': ''
}

project_json = {
    'mediaUrls': [],
    'hashtags': [],
    'id': 1,
    'stages': [],
    'title': 'title',
    'description': 'description',
    'category': 'category',
    'status': 'created',
    'fundedAmount': 0.0,
    'location': None,
    'ownerId': 3,
    'reviewerId': None,
    'walletId': None,
    'currentStageId': None,
    'finishDate': '',
    'createdAt': '',
    'updatedAt': ''
}


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test"]


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'MiddleSeedyFiuba :)'


# REVIEWS
@pytest.mark.asyncio
async def test_post_review(httpx_mock: HTTPXMock):
    body = {
        'reviewerId': 0,
        'projectId': 1
    }

    httpx_mock.add_response(method="POST", url='https://seedy-fiuba-users-api.herokuapp.com/reviews', json=review_json,
                            match_content=b'{"reviewerId": 0, "projectId": 1}')
    httpx_mock.add_response(method="PUT", url='https://seedy-fiuba-projects-api.herokuapp.com/api/project/1',
                            json=project_json,
                            match_content=b'{"status": "pending-reviewer"}')

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/reviews", json=body)

    print(response.text)
    assert response.status_code == 201
    assert response.json() == {'project': project_json, 'review': review_json}
