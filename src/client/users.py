import httpx
import os
from ..models.users import ReviewStatus, Review, User
from ..exceptions import MiddleException
from ..responses import ReviewPaginatedResponse, UsersPaginatedResponse, LoginResponse, AuthenticateResponse
from ..payloads import ReviewRequestPayload, CreateUserPayload, UpdateUserPayload, LoginPayload, GoogleLoginPayload
from ..repository import servers_repository as db
from pydantic import parse_obj_as

CLIENT_TIMEOUT = 60.0


async def create_review_request(payload: ReviewRequestPayload):
    url = f'{base_url()}/reviews'

    resp = await post(url, vars(payload))
    return parse_obj_as(Review, resp)


async def update_review_request(id: int, status: ReviewStatus):
    url = f'{base_url()}/reviews/{id}'

    body = {
        'status': status.value
    }

    resp = await put(url, body)
    return parse_obj_as(Review, resp)


async def search_review_request(params):
    url = f'{base_url()}/reviews'

    resp = await fetch(url, params)
    return parse_obj_as(ReviewPaginatedResponse, resp)


async def create_user(data: CreateUserPayload):
    url = f'{base_url()}/users'

    resp = await post(url, vars(data))
    return parse_obj_as(User, resp)


async def get_user(id: int):
    url = f'{base_url()}/users/{id}'

    resp = await fetch(url)
    return parse_obj_as(User, resp)


async def get_users(params: dict):
    url = f'{base_url()}/users'

    resp = await fetch(url, params)
    return parse_obj_as(UsersPaginatedResponse, resp)


async def update_user(user_id: int, payload: UpdateUserPayload):
    url = f'{base_url()}/users/{user_id}'

    resp = await put(url, parse_obj_to_dict(payload))
    return parse_obj_as(User, resp)


# AUTH
async def authenticate(token: str):
    url = f'{base_url()}/auth/authenticate'
    body = {
        'authToken': token
    }
    resp = await post(url, body)
    return parse_obj_as(AuthenticateResponse, resp)


async def login(data: LoginPayload):
    url = f'{base_url()}/auth/login'
    resp = await post(url, vars(data))
    return parse_obj_as(LoginResponse, resp)


async def google_login(data: GoogleLoginPayload):
    url = f'{base_url()}/auth/google_login'
    resp = await post(url, vars(data))
    return parse_obj_as(LoginResponse, resp)


async def fetch(url: str, params: dict = None):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        if params is not None:
            resp: httpx.Response = await client.get(url, params=params)
        else:
            resp: httpx.Response = await client.get(url)

        if resp.status_code >= 400:
            print(f"GET {url} failed: {resp.text}")
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

        print(resp.json())

    return resp.json()


async def post(url: str, data):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        resp: httpx.Response = await client.post(url, json=data)

        if resp.status_code >= 400:
            print(f"POST {url} failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

    return resp.json()


async def put(url: str, data: dict):
    async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
        resp: httpx.Response = await client.put(url, json=data)

        if resp.status_code >= 400:
            print(f"PUT {url} failed: " + resp.text)
            raise MiddleException(status=resp.status_code, detail=parse_error(resp))

    return resp.json()


def parse_obj_to_dict(obj):
    return {k: v for k, v in vars(obj).items() if v is not None}


def base_url():
    if os.environ['ENV'] != 'dev':
        return os.environ['USERS_BASE_URL']
    return db.ServerRepository().find({'name': os.environ['USERS_URL_KEY']})['url']


def parse_error(resp):
    response = resp.json()
    response['service'] = 'users'
    return response

