from pydantic import BaseModel
from enum import Enum


class Review(BaseModel):
    reviewerId: int
    projectId: int
    id: int
    status: str
    createdAt: str
    updatedAt: str


class ReviewStatus(str, Enum):
    approved = 'approved',
    rejected = 'rejected'
