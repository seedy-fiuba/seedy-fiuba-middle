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

user_json = {
    'name': 'Jack',
    'lastName': 'Mac',
    'email': 'jack.mack@gmail.com',
    'role': 'entrepreneur',
    'walletAddress': '0x000',
    'walletPrivateKey': '0x000',
    'createdAt': '',
    'updatedAt': ''
}

project_json = {
    'mediaUrls': [],
    'hashtags': [],
    'id': 1,
    'stages': [
        {
            'track': 'track1',
            'targetAmount': 0.001,
            'id': 0
        },
        {
            'track': 'track2',
            'targetAmount': 0.0001,
            'id': 1
        }
    ],
    'title': 'title',
    'description': 'description',
    'category': 'category',
    'status': 'pending-reviewer',
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

sc_project_json = {
    'txHash': '0x000123',
    'projectWalletId': 2,
    'stagesCost': [0.001, 0.0001],
    'projectOwnerAddress': "0x000",
    'projectReviewerAddress': "0x001",
    'projectStatus': 'FUNDING',
    'currentStage': 0,
    'missingAmount': 0.0011
}


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
    httpx_mock.add_response(method="GET", url='https://seedy-fiuba-projects-api.herokuapp.com/api/project/1',
                            json=project_json)

    # Get owner and review users
    user_json['role'] = 'entrepreneur'
    user_json['walletPrivateKey'] = '0x000'
    httpx_mock.add_response(method="GET", url='https://seedy-fiuba-users-api.herokuapp.com/users/' + str(project_json['ownerId']),
                            json=user_json)
    user_json['role'] = 'reviewer'
    user_json['walletPrivateKey'] = '0x001'
    httpx_mock.add_response(method="GET",
                            url='https://seedy-fiuba-users-api.herokuapp.com/users/' + str(review_json['reviewerId']),
                            json=user_json)

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