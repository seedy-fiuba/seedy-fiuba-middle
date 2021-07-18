from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class Status(str, Enum):
    PENDING_REVIEWER = 'pending-reviewer',
    STAGE_PENDING_REVIEWER = 'stage-pending-reviewer',
    IN_PROGRESS = 'in-progress',
    CREATED = 'created',
    FUNDING = 'funding',
    COMPLETED = 'completed'


class ProjectStage(BaseModel):
    track: str = None
    targetAmount: float = None
    id: int = None


class ProjectLocation(BaseModel):
    coordinates: List[float]
    type: str


class Project(BaseModel):
    mediaUrls: List[str] = []
    hashtags: List[str] = []
    id: int = None
    stages: List[ProjectStage] = []
    title: str = None
    description: str = None
    category: str = None
    status: str = None
    fundedAmount: float = None
    location: Optional[ProjectLocation]
    ownerId: int = None
    reviewerId: Optional[int]
    walletId: Optional[int]
    currentStageId: Optional[int]
    finishDate: str = None
    createdAt: str = None
    updatedAt: str = None


