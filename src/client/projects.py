import httpx
import os
from enum import Enum
from fastapi import HTTPException


class Status(Enum):
    PENDING_REVIEWER = 'pending-reviewer',
    IN_PROGRESS = 'in-progress'

async def getProject(projectId: int):
    url = f'{base_url()}/api/project/{projectId}'

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        if resp.status_code >= 400:
            print("Get project failed: " + resp.text)
            raise HTTPException(status_code=resp.status_code, detail=parse_error(resp))

        data = resp.json()

    return data

async def updateProjectStatus(projectId: int, status: Status):
    url = f'{base_url()}/api/project/{projectId}'

    body = {
        'status': status.value[0]
    }

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.put(url, json=body, headers=h)

        if resp.status_code >= 400:
            print("Update project failed: " + resp.text)
            raise HTTPException(status_code=resp.status_code, detail=parse_error(resp))

        data = resp.json()

    return data

def base_url():
    return os.environ['PROJECTS_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'projects'
    return response
