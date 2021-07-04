import httpx
import os
from ..models.users import ReviewStatus, Review
from ..exceptions import MiddleException
from ..responses import ReviewPaginatedResponse
from pydantic import parse_obj_as


async def create_review_request(payload):
    url = f'{base_url()}/reviews'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.post(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Create user review failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(Review, resp.json())

    return data


async def update_review_request(id: int, status: ReviewStatus):
    url = f'{base_url()}/reviews/{id}'

    body = {
        'status': status.value
    }

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.put(url, json=body)
        if resp.status_code >= 400:
            print("Update user review failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(Review, resp.json())

    return data


async def search_review_request(params):
    url = f'{base_url()}/reviews'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.get(url, params=params)
        if resp.status_code >= 400:
            print("Search user reviews failed with status " + str(resp.status_code) +  ":  " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(ReviewPaginatedResponse, resp.json())

    return data


def base_url():
    return os.environ['USERS_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'users'
    return response

