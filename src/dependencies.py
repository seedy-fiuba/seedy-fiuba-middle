import os
from fastapi import Header
from typing import Optional
from src.client import users as users_client

from src.exceptions import MiddleException


async def get_token_header(x_auth_token: Optional[str] = Header(None)):
    if x_auth_token is None and os.environ['ENV'] != 'dev':
        raise MiddleException(status=400, detail={'error': 'X-Auth-Token header is required to validate authorization'})
    if os.environ['ENV'] != 'dev':
        await users_client.authenticate(x_auth_token)
    return x_auth_token