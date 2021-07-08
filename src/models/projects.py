from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class Status(str, Enum):
    PENDING_REVIEWER = 'pending-reviewer',
    IN_PROGRESS = 'in-progress',
    CREATED = 'created',
    FUNDING = 'funding',
    COMPLETED = 'completed'


class ProjectStage(BaseModel):
    track: str
    targetAmount: float
    status: str


class ProjectLocation(BaseModel):
    coordinates: List[float]
    type: str


class Project(BaseModel):
    mediaUrls: List[str] = []
    hashtags: List[str] = []
    id: int
    stages: List[ProjectStage] = []
    title: str
    description: str
    category: str
    status: str
    fundedAmount: float
    location: Optional[ProjectLocation]
    ownerId: int
    reviewerId: Optional[int]
    finishDate: str
    createdAt: str
    updatedAt: str


