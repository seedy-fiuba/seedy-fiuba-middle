import pytest
from fastapi.testclient import TestClient
from src.main import app
from pytest_httpx import HTTPXMock

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

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'MiddleSeedyFiuba :)'


# REVIEWS
# @pytest.mark.asyncio
# async def test_post_review(mocker):
#     review_mock = Review(reviewerId=0,
#                          projectId=1,
#                          id=0,
#                          status='pending',
#                          createdAt='',
#                          updatedAt='')
#
#     project_mock = Project(mediaUrls=[],
#                            hashtags=[],
#                            id=1,
#                            stages=[],
#                            title='title',
#                            description='description',
#                            category='category',
#                            status='created',
#                            fundedAmount=0.0,
#                            location=None,
#                            ownerId=3,
#                            reviewerId=None,
#                            walletId=None,
#                            currentStageId=None,
#                            finishDate='',
#                            createdAt='',
#                            updatedAt='')
#
#     async def mock_request_review():
#         return review_response_mock
#
#     review_response_mock = ReviewResponseModel(project=project_mock, review=review_mock)
#     mocker.patch('src.controller.review_controller.request_review', return_value=mock_request_review())
#
#     body = {
#         'reviewerId': 0,
#         'projectId': 1
#     }
#
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post("/reviews", json=body)
#
#     assert response.status_code == 201
#     assert response.json() == review_response_mock
#
#     #response = client.post("/reviews", json=body)
#     #print(response.text)
#     #assert response.status_code == 201
#     #assert response.json() == review_response_mock

@pytest.mark.asyncio
def test_post_review(httpx_mock: HTTPXMock):
    body = {
        'reviewerId': 0,
        'projectId': 1
    }

    httpx_mock.add_response(method="POST", url='https://seedy-fiuba-users-api.herokuapp.com/reviews', json=review_json)
    httpx_mock.add_response(method="PUT", url='https://seedy-fiuba-projects-api.herokuapp.com/api/project/1', json=project_json)

    response = client.post("/reviews", json=body)
    print(response.text)
    assert response.status_code == 201