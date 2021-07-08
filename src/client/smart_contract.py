import httpx
import os
from .payloads.smart_contract import CreateSCProject
from .responses.smart_contract import CreateProjectResponse
from ..exceptions import MiddleException
from pydantic import parse_obj_as


async def create_project(payload: CreateSCProject):
    url = f"{base_url()}/project"

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp: httpx.Response = await client.post(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Create project in smart contract failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(CreateProjectResponse, resp.json())

    return data


def base_url():
    return os.environ['SMART_CONTRACT_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'smart_contract'
    return response
