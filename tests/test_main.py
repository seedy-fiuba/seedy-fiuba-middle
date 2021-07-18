from fastapi.testclient import TestClient
from src.main import app
from src.responses import ReviewResponseModel
from src.models.users import Review
from src.models.projects import Project

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'MiddleSeedyFiuba :)'


def test_post_review(mocker):
    review_mock = Review(reviewerId=0,
                         projectId=1,
                         id=0,
                         status='pending',
                         createdAt='',
                         updatedAt='')

    project_mock = Project(mediaUrls=[],
                           hashtags=[],
                           id=1,
                           stages=[],
                           title='title',
                           description='description',
                           category='category',
                           status='created',
                           fundedAmount=0.0,
                           location=None,
                           ownerId=3,
                           reviewerId=None,
                           walletId=None,
                           currentStageId=None,
                           finishDate='',
                           createdAt='',
                           updatedAt='')

    review_response_mock = ReviewResponseModel(project=project_mock, review=review_mock)
    mocker.patch('src.controller.review_controller.request_review', return_value=review_response_mock)

    body = {
        'reviewerId': 0,
        'projectId': 1
    }

    response = client.post("/reviews", json=body)
    print(response.text)
    assert response.status_code == 201
    assert response.json() == review_response_mock
