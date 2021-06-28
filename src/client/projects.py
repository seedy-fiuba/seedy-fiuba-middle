import httpx
import os
from ..models.projects import Status, Project
from ..exceptions import MiddleException
from pydantic import parse_obj_as


async def get_project(projectId: int):
    url = f'{base_url()}/api/project/{projectId}'

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        if resp.status_code >= 400:
            print("Get project failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        data = parse_obj_as(Project, resp.json())

    return data


async def update_project(projectId: int, data: dict):
    url = f'{base_url()}/api/project/{projectId}'

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.put(url, json=data, headers=h)

        if resp.status_code >= 400:
            print("Update project failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        data = parse_obj_as(Project, resp.json())

    return data

def base_url():
    return os.environ['PROJECTS_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'projects'
    return response
