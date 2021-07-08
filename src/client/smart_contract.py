import httpx
import os
from .payloads.smart_contract import CreateSCProject, FundSCProject, AcceptSCProjectStage
from .responses.smart_contract import CreateProjectResponse, FundProjectResponse, AcceptStageResponse
from ..responses import WalletBalanceResponse
from ..exceptions import MiddleException
from pydantic import parse_obj_as

CLIENT_TIMEOUT = 300.0


async def create_project(payload: CreateSCProject):
    url = f"{base_url()}/project"

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        resp: httpx.Response = await client.post(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Create project in smart contract failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(CreateProjectResponse, resp.json())

    return data


async def fund_project(wallet_id: int, payload: FundSCProject):
    url = f"{base_url()}/fund/projects/{wallet_id}"


    print(f"Funding SC project with ID: {wallet_id} and payload: {payload.dict()}")
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        resp: httpx.Response = await client.post(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Fund project in smart contract failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(FundProjectResponse, resp.json())

    return data


async def accept_stage(wallet_id: int, payload: AcceptSCProjectStage):
    url = f"{base_url()}/projects/{wallet_id}"

    print(f"Accepting stage SC project with ID: {wallet_id} and payload: {payload.dict()}")
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        resp: httpx.Response = await client.put(url, json=vars(payload))
        if resp.status_code >= 400:
            print("Accept project stage in smart contract failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(AcceptStageResponse, resp.json())

    return data


async def get_balance(user_private_key: str):
    url = f"{base_url()}/wallet/{user_private_key}"

    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        resp: httpx.Response = await client.get(url)
        if resp.status_code >= 400:
            print("Get wallet balance from smart contract failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))
        data = parse_obj_as(WalletBalanceResponse, resp.json())

    return data

def base_url():
    return os.environ['SMART_CONTRACT_BASE_URL']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'smart_contract'
    return response
