import pytest
from src.main import app
from pytest_httpx import HTTPXMock
from httpx import AsyncClient
from .mocks import *

user_json = user_template.copy()
project_json = project_template.copy()
fund_project_response = fund_project_response_template.copy()
accept_stage_response = accept_stage_response_template.copy()


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test"]


@pytest.mark.asyncio
async def test_get_project(httpx_mock: HTTPXMock):
    mock_get_project(httpx_mock, project_json['id'], project_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/projects/{project_json['id']}")

    print('response: ' + response.text)
    assert response.status_code == 200
    assert response.json() == project_json


@pytest.mark.asyncio
async def test_put_project(httpx_mock: HTTPXMock):
    body = {
                'status': 'funding',
                'missingAmount': fund_project_response['missingAmount']
            }
    mock_update_project(httpx_mock, project_json['id'], body, project_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/projects/{project_json['id']}", json=body)

    print('response: ' + response.text)
    assert response.status_code == 200
    assert response.json() == project_json


@pytest.mark.asyncio
async def test_fund_project(httpx_mock: HTTPXMock):
    body = {
        'funderId': 5,
        'amount': 0.001
    }

    # Mock get funder user
    user_json['role'] = 'sponsor'
    mock_get_user(httpx_mock, body['funderId'], user_json)

    # Mock get project
    project_json['status'] = 'funding'
    mock_get_project(httpx_mock, project_json['id'], project_json)

    # Mock fund smart contract
    fund_project_response['projectStatus'] = "FUNDING"
    mock_fund_sc_project(httpx_mock,
                         project_json['walletId'],
                         {
                             'funderPrivateKey': user_json['walletPrivateKey'],
                             'amount': body['amount']
                         }, fund_project_response)

    # Mock fund projects api
    mock_fund_project(httpx_mock, project_json['id'],
                      {
                          'funderId': body['funderId'],
                          'currentFundedAmount': body['amount'],
                          'txHash': fund_project_response['txHash']
                      })

    # Mock update project
    mock_update_project(httpx_mock, project_json['id'],
                        {
                            'status': 'funding',
                            'missingAmount': fund_project_response['missingAmount']
                        }, project_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/projects/{project_json['id']}/fund", json=body)

    print('response: ' + response.text)
    assert response.status_code == 200
    assert response.text == ''


@pytest.mark.asyncio
async def test_accept_stage(httpx_mock: HTTPXMock):
    body = {
        'reviewerId': 20
    }
    stage_id = 1

    # Mock get reviewer user
    user_json['role'] = 'reviewer'
    mock_get_user(httpx_mock, body['reviewerId'], user_json)

    # Mock get project
    project_json['status'] = 'stage-pending-reviewer'
    mock_get_project(httpx_mock, project_json['id'], project_json)

    # Mock accept stage in smart contract
    mock_sc_accept_stage(httpx_mock, project_json['walletId'],
                         {
                             'reviewerPrivateKey': user_json['walletPrivateKey'],
                             'completedStage': stage_id + 1
                         }, accept_stage_response)

    assert accept_stage_response['projectStatus'] == 'IN_PROGRESS'
    # Mock update project
    project_json['status'] = 'in-progress'
    mock_update_project(httpx_mock, project_json['id'],
                        {
                            'status': 'in-progress',
                            'currentStageId': accept_stage_response['stageCompleted']
                        }, project_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/projects/{project_json['id']}/stages/{stage_id}/accept", json=body)

    print(response.text)
    assert response.status_code == 200
    assert response.text == ''


@pytest.mark.asyncio
async def test_request_stage_review(httpx_mock: HTTPXMock):
    # Mock update project
    project_json['status'] = 'stage-pending-reviewer'
    mock_update_project(httpx_mock, project_json['id'],
                        {
                            'status': 'stage-pending-reviewer'
                        }, project_json)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/projects/{project_json['id']}/review")

    print(response.text)
    assert response.status_code == 200
    assert response.json() == project_json