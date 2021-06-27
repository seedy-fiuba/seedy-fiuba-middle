from fastapi import Header, HTTPException
from typing import Optional


async def getTokenHeader(x_auth_token: Optional[str] = Header(None)):
    if x_auth_token is None:
        raise HTTPException(status_code=400, detail="X-Token header is required to validate authorization")