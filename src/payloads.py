from pydantic import BaseModel
from .models.users import ReviewStatus
from typing import Optional


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


# Servers
class ServerCreatePayload(BaseModel):
    name: str
    url: str
    description: str


class ServerUpdatePayload(BaseModel):
    url: str