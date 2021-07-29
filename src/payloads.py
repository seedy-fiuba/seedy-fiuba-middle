from pydantic import BaseModel
from .models.users import ReviewStatus
from typing import List


# Reviews
class ReviewRequestPayload(BaseModel):
    reviewerId: int
    projectId: int


class ReviewUpdatePayload(BaseModel):
    status: ReviewStatus


# Projects
class FundProjectPayload(BaseModel):
    funderId: int
    amount: float


class AcceptStagePayload(BaseModel):
    reviewerId: int


class TransferFundsPayload(BaseModel):
    destinationAddress: str
    amount: float


class CreateProjectStagePayload(BaseModel):
    track: str
    targetAmount: float


class CreateProjectLocationPayload(BaseModel):
    x: float
    y: float


class CreateProjectPayload(BaseModel):
    title: str
    description: str
    category: str
    mediaUrls: List[str]
    stages: List[CreateProjectStagePayload]
    location: CreateProjectLocationPayload
    hashtags: List[str]
    ownerId: int = None
    reviewerId: int = None
    finishDate: str


# Servers
class ServerCreatePayload(BaseModel):
    name: str
    url: str
    description: str


class ServerUpdatePayload(BaseModel):
    url: str