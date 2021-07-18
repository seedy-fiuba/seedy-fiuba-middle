from pydantic import BaseModel
from typing import List
from enum import Enum


class ProjectStatus(str, Enum):
    FUNDING = 'FUNDING',
    IN_PROGRESS = 'IN_PROGRESS',
    COMPLETED = 'COMPLETED'


class CreateProjectResponse(BaseModel):
    txHash: str = None
    projectWalletId: int = None
    stagesCost: List[float] = []
    projectOwnerAddress: str = None
    projectReviewerAddress: str = None
    projectStatus: ProjectStatus = None
    currentStage: int = None
    missingAmount: float = None


class FundProjectResponse(BaseModel):
    txHash: str = None
    projectWalletId: str = None
    fundsReceived: str = None
    funderAddress: str = None
    missingAmount: str = None
    projectStatus: ProjectStatus = None


class AcceptStageResponse(BaseModel):
    txHash: str = None
    projectWalletId: int = None
    stageCompleted: int = None
    projectStatus: ProjectStatus = None

