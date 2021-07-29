from ..payloads import CreateUserPayload, UpdateUserPayload
from ..client import users as users_client


async def create_user(payload: CreateUserPayload):
    return await users_client.create_user(payload)


async def get_users(params: dict):
    for key, value in dict(params).items():
        if value is None:
            del params[key]

    return await users_client.get_users(params)


async def get_user_by_id(user_id: int):
    return await users_client.get_user(user_id)


async def update_user(user_id: int, payload: UpdateUserPayload):
    return await users_client.update_user(user_id, payload)

