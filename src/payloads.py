from pydantic import BaseModel
from .models.users import ReviewStatus


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


