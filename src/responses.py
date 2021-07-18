from .models import projects, users
from pydantic import BaseModel
from typing import List


class ReviewResponseModel(BaseModel):
    project: projects.Project = None
    review: users.Review


class ReviewPaginatedResponse(BaseModel):
    size: int
    results: List[users.Review]


class ProjectPaginatedResponse(BaseModel):
    size: int
    results: List[projects.Project]


class ReviewProjectSearchResponse(BaseModel):
    size: int
    results: List[ReviewResponseModel]


class WalletBalanceResponse(BaseModel):
    balance: float

