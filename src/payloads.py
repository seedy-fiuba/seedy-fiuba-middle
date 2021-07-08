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
    amount: int


class AcceptStagePayload(BaseModel):
    reviewerId: int

