from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from ..controller import projects_controller
from ..payloads import FundProjectPayload, AcceptStagePayload
from ..dependencies import get_token_header
from typing import List
from ..models.projects import Project


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.get('/', response_model=List[Project])
async def get_projects(x_auth_token: str = Depends(get_token_header)):
    return await projects_controller.get_projects(x_auth_token)


# @router.get('/search')
# async def search_projects(): # TODO add params
#     return await projects_controller.search_projects()
#
#
# @router.get('/{project_id}')
# async def get_project_by_id(project_id: int):
#     return await projects_controller.get_project_by_id(project_id)
#
#
# @router.post('/')
# async def create_project(): # TODO add payload
#     return await projects_controller.create_project()
#
#
# @router.put('/{project_id}')
# async def update_project(project_id: int): # TODO add payload
#     return await projects_controller.update_project(project_id)


@router.post('/{project_id}/fund', response_class=PlainTextResponse)
async def fund_project(project_id: int, payload: FundProjectPayload):
    return await projects_controller.fund_project(project_id, payload)


@router.post('/{project_id}/stages/{stage_id}/accept', response_class=PlainTextResponse)
async def accept_stage(project_id: int, stage_id: int, payload: AcceptStagePayload):
    return await projects_controller.accept_stage(project_id, stage_id, payload)


@router.post('/{project_id}/review')
async def request_stage_review(project_id: int):
    return await projects_controller.request_stage_review(project_id)