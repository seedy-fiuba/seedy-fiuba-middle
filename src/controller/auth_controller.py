from src.payloads import LoginPayload, GoogleLoginPayload, AuthenticatePayload
from ..client import users as users_client


async def login(payload: LoginPayload):
    return await users_client.login(payload)


async def google_login(payload: GoogleLoginPayload):
    return await users_client.google_login(payload)


async def authenticate(payload: AuthenticatePayload):
    return await users_client.authenticate(payload.authToken)

