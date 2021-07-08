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
    projectStatus: str = None
    currentStage: int = None
    missingAmount: float = None

