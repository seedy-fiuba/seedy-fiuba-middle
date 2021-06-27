import httpx
import os
from ..exceptions import MiddleException
from pydantic import BaseModel


class Review(BaseModel):
    reviewerId: int
    projectId: int
    id: int
    status: str
    createdAt: str
    updatedAt: str


async def create_review_request(payload):
    url = f'{base_url()}/reviews'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.post(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Create user review failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = resp.json()

    return data


async def update_review_request(id: int, status: str):
    url = f'{base_url()}/reviews/{id}'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.put(url, json={status: status})
        if resp.status_code >= 400:
            print("Update user review failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = resp.json()

    return data


async def search_review_request(params):
    url = f'{base_url()}/reviews'
    if len(params) > 0:
        url += '?'
        count = 0
    for key in params:
        count += 1
        url += key + '=' + params[key]
        if count < len(params):
            url += '&'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.get(url)
        if resp.status_code >= 400:
            print("Search user reviews failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = resp.json()

    return data


def base_url():
    return os.environ['USERS_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'users'
    return response

