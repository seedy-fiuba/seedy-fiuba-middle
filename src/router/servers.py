from fastapi import APIRouter, status as HTTPStatus
from ..payloads import ServerCreatePayload, ServerUpdatePayload
from ..controller import servers_controller
from ..models.servers import Server
from typing import List


router = APIRouter(
    prefix="/servers",
    tags=["servers"]
)


@router.post('', response_model=Server, status_code=HTTPStatus.HTTP_201_CREATED)
async def create_server(payload: ServerCreatePayload):
    return await servers_controller.create_server(payload)


@router.get('', response_model=List[Server])
async def get_servers():
    return await servers_controller.get_servers()


@router.get('/{server_id}', response_model=Server)
async def get_server(server_id: int):
    return await servers_controller.get_server(server_id)


@router.put('/{server_id}', response_model=Server)
async def update_server(server_id: int, payload: ServerUpdatePayload):
    return await servers_controller.update_server(server_id, payload)