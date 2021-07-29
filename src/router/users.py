from fastapi import APIRouter, status as HTTPStatus, Depends

from ..dependencies import get_token_header
from ..models.users import User
from ..payloads import CreateUserPayload, UpdateUserPayload
from ..responses import UsersPaginatedResponse
from ..controller import users_controller
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)]
)


@router.post('', response_model=User, status_code=HTTPStatus.HTTP_201_CREATED)
async def create_user(payload: CreateUserPayload):
    return await users_controller.create_user(payload)


@router.get('', response_model=UsersPaginatedResponse)
async def get_users(size: Optional[str] = None,
                    page: Optional[str] = None,
                    role: Optional[str] = None):
    params = {
        'size': size,
        'page': page,
        'role': role
    }
    return await users_controller.get_users(params)


@router.get('/{user_id}', response_model=User)
async def get_user_by_id(user_id: int):
    return await users_controller.get_user_by_id(user_id)


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, payload: UpdateUserPayload):
    return await users_controller.update_user(user_id, payload)