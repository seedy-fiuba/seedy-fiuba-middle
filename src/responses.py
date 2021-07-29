from .models import projects, users
from pydantic import BaseModel
from typing import List


class ReviewResponseModel(BaseModel):
    project: projects.Project = None
    review: users.Review


class ReviewPaginatedResponse(BaseModel):
    size: int
    results: List[users.Review] = []


class ProjectPaginatedResponse(BaseModel):
    size: int
    results: List[projects.Project] = []


class ReviewProjectSearchResponse(BaseModel):
    size: int
    results: List[ReviewResponseModel] = []


class WalletBalanceResponse(BaseModel):
    balance: float


class ContractResponseModel(BaseModel):
    project: projects.Project = None
    contract: projects.Contract


class ContractProjectSearchResponse(BaseModel):
    totalItems: int
    results: List[ContractResponseModel]
    totalPages: int
    currentPage: int


class UsersPaginatedResponse(BaseModel):
    totalItems: int
    users: List[users.User]
    totalPages: int
    currentPage: int

