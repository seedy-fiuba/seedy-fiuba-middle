import pytest
from src.main import app
from httpx import AsyncClient
from .mocks import *

review_json = review_template.copy()
user_json = user_template.copy()
project_json = project_template.copy()
sc_project_json = sc_project_template.copy()


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test"]


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


@pytest.mark.asyncio
async def test_reject_review(httpx_mock: HTTPXMock):
    body = {
        'status': 'rejected'
    }
    review_json['status'] = 'rejected'
    project_json['status'] = 'created'

    httpx_mock.add_response(method="PUT", url='https://seedy-fiuba-users-api.herokuapp.com/reviews/0',
                            json=review_json,
                            match_content=b'{"status": "rejected"}')
    httpx_mock.add_response(method="PUT", url='https://seedy-fiuba-projects-api.herokuapp.com/api/project/1',
                            json=project_json,
                            match_content=b'{"status": "created"}')

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/reviews/0", json=body)

    print(response.text)
    assert response.status_code == 200
    assert response.json() == {'project': project_json, 'review': review_json}


@pytest.mark.asyncio
async def test_approve_review(httpx_mock: HTTPXMock):
    body = {
        'status': 'approved'
    }
    review_json['status'] = 'approved'
    project_json['status'] = 'created'

    # Update review status
    httpx_mock.add_response(method="PUT", url='https://seedy-fiuba-users-api.herokuapp.com/reviews/0',
                            json=review_json,
                            match_content=b'{"status": "approved"}')

    # Get project to know who is de owner
    mock_get_project(httpx_mock, 1, project_json)

    # Get owner and review users
    user_json['role'] = 'entrepreneur'
    user_json['walletPrivateKey'] = '0x000'
    mock_get_user(httpx_mock, project_json['ownerId'], user_json)

    user_json['role'] = 'reviewer'
    user_json['walletPrivateKey'] = '0x001'
    mock_get_user(httpx_mock, review_json['reviewerId'], user_json)

    # Create project in smart contract
    httpx_mock.add_response(method="POST", url='https://seedy-fiuba-smart-contract.herokuapp.com/project',
                            json=sc_project_json,
                            match_content=b'{"ownerPrivateKey": "0x000", "reviewerPrivateKey": "0x001", "stagesCost": [0.001, 0.0001]}')

    # Update project
    httpx_mock.add_response(method="PUT", url='https://seedy-fiuba-projects-api.herokuapp.com/api/project/1',
                            json=project_json,
                            match_content=str.encode('{"status": "funding", "currentStageId": ' + str(sc_project_json['currentStage'])
                                          + ', "walletId": ' + str(sc_project_json['projectWalletId'])
                                          + ', "reviewerId": ' + str(review_json['reviewerId']) + '}'))

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/reviews/0", json=body)

    print(response.text)
    assert response.status_code == 200
    assert response.json() == {'project': project_json, 'review': review_json}


@pytest.mark.asyncio
async def test_get_reviews(httpx_mock: HTTPXMock):
    review_response_mock = {
        'size': 1,
        'results': [
            review_json
        ]
    }

    project_response_mock = {
        'size': 1,
        'results': [
            project_json
        ]
    }
    httpx_mock.add_response(method="GET",
                            url="https://seedy-fiuba-users-api.herokuapp.com/reviews",
                            json=review_response_mock)
    httpx_mock.add_response(method="GET",
                            url="https://seedy-fiuba-projects-api.herokuapp.com/api/project/search?id=1",
                            json=project_response_mock)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/reviews")

    print(response.text)
    assert response.status_code == 200
    assert response.json() == {
        'size': 1,
        'results': [
            {
                'project': project_json,
                'review': review_json
            }
        ]
    }