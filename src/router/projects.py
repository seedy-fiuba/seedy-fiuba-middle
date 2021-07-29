from fastapi import APIRouter, status as HTTPStatus
from fastapi.responses import PlainTextResponse
from ..controller import projects_controller
from ..payloads import FundProjectPayload, AcceptStagePayload, \
    CreateProjectPayload
from ..client.payloads.projects import UpdateProjectPayload
from ..responses import ProjectPaginatedResponse
from typing import List
from ..models.projects import Project
from typing import Optional


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.get('', response_model=List[Project])
async def get_projects():
    return await projects_controller.get_projects()


@router.get('/search', response_model=ProjectPaginatedResponse)
async def search_projects(status: Optional[str] = None,
                          category: Optional[str] = None,
                          locationX: Optional[str] = None,
                          locationY: Optional[str] = None,
                          ownerId: Optional[str] = None,
                          hashtags: Optional[str] = None,
                          id: Optional[str] = None):
    params = {
        'status': status,
        'category': category,
        'locationX': locationX,
        'locationY': locationY,
        'ownerId': ownerId,
        'hashtags': hashtags,
        'id': id
    }
    return await projects_controller.search_projects(params)


@router.get('/{project_id}', response_model=Project)
async def get_project_by_id(project_id: int):
    return await projects_controller.get_project_by_id(project_id)


@router.post('', response_model=Project, status_code=HTTPStatus.HTTP_201_CREATED)
async def create_project(payload: CreateProjectPayload):
    return await projects_controller.create_project(payload)


@router.put('/{project_id}', response_model=Project)
async def update_project(project_id: int, payload: UpdateProjectPayload):
    return await projects_controller.update_project(project_id, payload)


@router.post('/{project_id}/fund', response_class=PlainTextResponse)
async def fund_project(project_id: int, payload: FundProjectPayload):
    return await projects_controller.fund_project(project_id, payload)


@router.post('/{project_id}/stages/{stage_id}/accept', response_class=PlainTextResponse)
async def accept_stage(project_id: int, stage_id: int, payload: AcceptStagePayload):
    return await projects_controller.accept_stage(project_id, stage_id, payload)


@router.post('/{project_id}/review')
async def request_stage_review(project_id: int):
    return await projects_controller.request_stage_review(project_id)