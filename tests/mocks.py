from pytest_httpx import HTTPXMock
from src.client.users import base_url as users_base_url
from src.client.projects import base_url as projects_base_url
from src.client.smart_contract import base_url as sc_base_url
import json

review_template = {
    'reviewerId': 0,
    'projectId': 1,
    'id': 0,
    'status': 'pending',
    'createdAt': '',
    'updatedAt': ''
}

user_template = {
    'id':10,
    'name': 'Jack',
    'lastName': 'Mac',
    'email': 'jack.mack@gmail.com',
    'role': 'entrepreneur',
    'walletAddress': '0x000',
    'walletPrivateKey': '0x000',
    'description': '',
    'firebaseToken': '',
    'createdAt': '',
    'updatedAt': ''
}

project_template = {
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
    'walletId': 10,
    'currentStageId': None,
    'finishDate': '',
    'createdAt': '',
    'updatedAt': ''
}

sc_project_template = {
    'txHash': '0x000123',
    'projectWalletId': project_template['walletId'],
    'stagesCost': [0.001, 0.0001],
    'projectOwnerAddress': "0x000",
    'projectReviewerAddress': "0x001",
    'projectStatus': 'FUNDING',
    'currentStage': 0,
    'missingAmount': 0.0011
}

fund_project_response_template = {
    'txHash': sc_project_template['txHash'],
    'projectWalletId': sc_project_template['projectWalletId'],
    'fundsReceived': 0.001,
    'funderAddress': user_template['walletPrivateKey'],
    'missingAmount': sc_project_template['missingAmount'],
    'projectStatus': 'FUNDING'
}

accept_stage_response_template = {
    'txHash': sc_project_template['txHash'],
    'projectWalletId': sc_project_template['projectWalletId'],
    'stageCompleted': 1,
    'projectStatus': 'IN_PROGRESS'
}

balance_template = {
    'balance': 0.1
}

contract_template = {
    "projectId": 1,
    "funderId": 32,
    "currentFundedAmount": 0.000001,
    "txHash": "0x1aa945a5f47b16ae76539af4df3497c9aedf04c34408fd6055b0d4ff78102854",
    "createdAt": "2021-07-08T21:14:53.934Z",
    "updatedAt": "2021-07-08T21:14:53.934Z"
}

# PROJECTS
def mock_get_project(httpx_mock: HTTPXMock, project_id: int, response: dict):
    httpx_mock.add_response(method="GET",
                            url= projects_base_url() + f'/api/project/{project_id}',
                            json=response)


def mock_update_project(httpx_mock: HTTPXMock, project_id: int, body: dict, response: dict):
    httpx_mock.add_response(method="PUT",
                            url=projects_base_url() + f'/api/project/{project_id}',
                            json=response,
                            match_content=str.encode(json.dumps(body)))


def mock_fund_project(httpx_mock: HTTPXMock, project_id: int, body: dict):
    httpx_mock.add_response(method="POST",
                            url=projects_base_url() + f'/api/project/{project_id}/fund',
                            match_content=str.encode(json.dumps(body)))


# USERS
def mock_get_user(httpx_mock: HTTPXMock, user_id: int, response: dict):
    httpx_mock.add_response(method="GET",
                            url= users_base_url() + f'/users/{user_id}',
                            json=response)


def mock_update_user(httpx_mock: HTTPXMock, user_id: int, body: dict, response: dict):
    httpx_mock.add_response(method="PUT",
                            url=users_base_url() + f'/users/{user_id}',
                            json=response,
                            match_content=str.encode(json.dumps(body)))


# SMART CONTRACT
def mock_fund_sc_project(httpx_mock: HTTPXMock, project_wallet_id: int, body: dict, response: dict):
    httpx_mock.add_response(method="POST",
                            url=sc_base_url() + f'/fund/projects/{project_wallet_id}',
                            json=response,
                            match_content=str.encode(json.dumps(body)))


def mock_sc_accept_stage(httpx_mock: HTTPXMock, project_wallet_id: int, body: dict, response: dict):
    httpx_mock.add_response(method="PUT",
                            url=sc_base_url() + f'/projects/{project_wallet_id}',
                            json=response,
                            match_content=str.encode(json.dumps(body)))


def mock_sc_get_balance(httpx_mock: HTTPXMock, user_private_key: str, response: dict):
    httpx_mock.add_response(method="GET",
                            url=sc_base_url() + f'/wallet/{user_private_key}',
                            json=response)


def mock_sc_transfer_funds(httpx_mock: HTTPXMock, body: dict):
    httpx_mock.add_response(method="POST",
                            url=sc_base_url() + f'/transfer/funds',
                            match_content=str.encode(json.dumps(body)))