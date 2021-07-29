from fastapi import APIRouter
from ..payloads import LoginPayload, GoogleLoginPayload, AuthenticatePayload
from ..responses import LoginResponse, AuthenticateResponse
from ..controller import auth_controller

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post('/login', response_model=LoginResponse)
async def login(payload: LoginPayload):
    return await auth_controller.login(payload)


@router.post('/google_login', response_model=LoginResponse)
async def google_login(payload: GoogleLoginPayload):
    return await auth_controller.google_login(payload)


@router.post('/authenticate', response_model=AuthenticateResponse)
async def authenticate(payload: AuthenticatePayload):
    return await auth_controller.authenticate(payload)

