from .models import projects, users
from pydantic import BaseModel
from typing import List


# Reviews
class ReviewResponseModel(BaseModel):
    project: projects.Project = None
    review: users.Review


class ReviewPaginatedResponse(BaseModel):
    size: int
    results: List[users.Review] = []


class ReviewProjectSearchResponse(BaseModel):
    size: int
    results: List[ReviewResponseModel] = []


# Projects
class ProjectPaginatedResponse(BaseModel):
    size: int
    results: List[projects.Project] = []


# Wallet
class WalletBalanceResponse(BaseModel):
    balance: float


# Contracts
class ContractResponseModel(BaseModel):
    project: projects.Project = None
    contract: projects.Contract


class ContractProjectSearchResponse(BaseModel):
    totalItems: int
    results: List[ContractResponseModel]
    totalPages: int
    currentPage: int


# Users
class UsersPaginatedResponse(BaseModel):
    totalItems: int
    users: List[users.User]
    totalPages: int
    currentPage: int


# Auth
class LoginResponse(BaseModel):
    user: users.User
    token: str


class AuthenticateResponse(BaseModel):
    message: str
    identity: dict

