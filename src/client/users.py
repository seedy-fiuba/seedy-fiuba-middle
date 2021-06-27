import httpx
import os
from fastapi import HTTPException


async def createReviewRequest(payload):
    url = f'{base_url()}/reviews'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.post(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Create user review failed: " + resp.text)
            raise HTTPException(status_code=resp.status_code, detail=parse_error(resp))
        data = resp.json()

    return data

async def updateReviewRequest(id: int, status: str):
    url = f'{base_url()}/reviews/{id}'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.put(url, json={status: status})
        if resp.status_code >= 400:
            print("Update user review failed: " + resp.text)
            raise HTTPException(status_code=resp.status_code, detail=parse_error(resp))
        data = resp.json()

    return data

async def searchReviewRequest(params):
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
            raise HTTPException(status_code=resp.status_code, detail=parse_error(resp))
        data = resp.json()

    return data

def base_url():
    return os.environ['USERS_BASE_URL']

def parse_error(resp):
    response = resp.json()
    response['service'] = 'users'
    return response