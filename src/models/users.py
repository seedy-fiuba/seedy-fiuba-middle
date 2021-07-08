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


class Role(str, Enum):
    reviewer = 'reviewer',
    sponsor = 'sponsor',
    entrepreneur = 'entrepreneur',
    admin = 'admin'


class User(BaseModel):
    name: str
    lastName: str
    email: str
    role: Role
    walletAddress: str = None
    walletPrivateKey: str = None
    createdAt: str
    updatedAt: str

