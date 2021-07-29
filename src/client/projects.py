import httpx
import os
from ..models.projects import Project
from ..exceptions import MiddleException
from ..responses import ProjectPaginatedResponse
from .responses import projects as projects_responses
from .payloads.projects import UpdateProjectPayload, FundProjectClientPayload
from pydantic import parse_obj_as
from typing import List

CLIENT_TIMEOUT = 60.0


async def get_projects():
    url = f'{base_url()}/api/project'

    resp = await fetch(url)
    return parse_obj_as(List[Project], resp)


async def get_project(projectId: int):
    url = f'{base_url()}/api/project/{projectId}'

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        if resp.status_code >= 400:
            print("Get project failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        data = parse_obj_as(Project, resp.json())

    return data


async def update_project(projectId: int, data: UpdateProjectPayload):
    url = f'{base_url()}/api/project/{projectId}'

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.put(url, json={k: v for k, v in vars(data).items() if v is not None}, headers=h)

        if resp.status_code >= 400:
            print("Update project failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        data = parse_obj_as(Project, resp.json())

    return data


async def search_project(params):
    url = f'{base_url()}/api/project/search'

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h,  params=params)
        if resp.status_code >= 400:
            print("Search projects failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(ProjectPaginatedResponse, resp.json())

    return data


async def fund_project(projectId: int, data: FundProjectClientPayload):
    url = f'{base_url()}/api/project/{projectId}/fund'

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.post(url, json={k: v for k, v in vars(data).items() if v is not None},
                                                headers=h)

        if resp.status_code >= 400:
            print("Fund project in projects api failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        #data = parse_obj_as(Project, resp.json())

    #return data


async def search_contracts(params):
    url = f'{base_url()}/api/contracts'

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, params=params, headers=h)
        if resp.status_code >= 400:
            print(f"Search contracts failed with status {resp.status_code}: {resp.text}")
            raise MiddleException(status= resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(projects_responses.ContractPaginatedResponse, resp.json())

    return data


async def fetch(url: str):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        if resp.status_code >= 400:
            print(f"GET {url} failed: {resp.text}")
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        return resp.json()


def base_url():
    return os.environ['PROJECTS_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'projects'
    return response
