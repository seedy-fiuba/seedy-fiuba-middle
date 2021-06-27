from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import getTokenHeader
from ..client.projects import getProject


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(getTokenHeader)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getProjects():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/search")
async def searchProjects():
    return {"username": "fakecurrentuser"}


@router.get("/{projectId}", responses={404: {"description": "Not found"}})
async def getProjectById(projectId: int):
    return await getProject(projectId)


@router.post("/")
async def projectCreation():
    return {"project": "new project"}


@router.put("/{projectId}")
async def projectUpdate(projectId: int):
    return {"project": f"updated project {projectId}"}
