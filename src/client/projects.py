import httpx
import os
from ..models.projects import Project
from ..exceptions import MiddleException
from ..responses import ProjectPaginatedResponse
from ..payloads import CreateProjectPayload
from .responses import projects as projects_responses
from .payloads.projects import UpdateProjectPayload, FundProjectClientPayload
from pydantic import parse_obj_as, BaseModel
from typing import List

CLIENT_TIMEOUT = 60.0


async def get_projects():
    url = f'{base_url()}/api/project'

    resp = await fetch(url)
    return parse_obj_as(List[Project], resp)


async def get_project(project_id: int):
    url = f'{base_url()}/api/project/{project_id}'

    resp = await fetch(url)
    return parse_obj_as(Project, resp)


async def create_project(data: CreateProjectPayload):
    url = f'{base_url()}/api/project'

    resp = await post(url, data.dict())
    return parse_obj_as(Project, resp)


async def update_project(project_id: int, data: UpdateProjectPayload):
    url = f'{base_url()}/api/project/{project_id}'

    resp = await put(url, parse_obj_to_dict(data))
    return parse_obj_as(Project, resp)


async def search_projects(params):
    url = f'{base_url()}/api/project/search'

    resp = await fetch(url, params)
    return parse_obj_as(ProjectPaginatedResponse, resp)


async def fund_project(project_id: int, data: FundProjectClientPayload):
    url = f'{base_url()}/api/project/{project_id}/fund'
    await post(url, parse_obj_to_dict(data))


async def search_contracts(params):
    url = f'{base_url()}/api/contracts'

    resp = await fetch(url, params)
    return parse_obj_as(projects_responses.ContractPaginatedResponse, resp)


async def fetch(url: str, params: dict = None):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        if params is not None:
            resp: httpx.Response = await client.get(url, headers=h, params=params)
        else:
            resp: httpx.Response = await client.get(url, headers=h)

        if resp.status_code >= 400:
            print(f"GET {url} failed: {resp.text}")
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        return resp.json()


async def post(url: str, data):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.post(url, json=data, headers=h)

        if resp.status_code >= 400:
            print(f"POST {url} failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

    return resp.json()


async def put(url: str, data: dict):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.put(url, json=data, headers=h)

        if resp.status_code >= 400:
            print(f"PUT {url} failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

    return resp.json()


def parse_obj_to_dict(obj):
    return {k: v for k, v in vars(obj).items() if v is not None}


def base_url():
    return os.environ['PROJECTS_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'projects'
    return response
