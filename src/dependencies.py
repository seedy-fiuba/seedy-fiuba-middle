from fastapi import Header
from typing import Optional

from src.exceptions import MiddleException


async def get_token_header(x_auth_token: Optional[str] = Header(None)):
    if x_auth_token is None:
        raise MiddleException(status=400, detail={'error': 'X-Auth-Token header is required to validate authorization'})
    return x_auth_token