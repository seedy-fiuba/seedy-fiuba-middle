from .models import projects, users
from pydantic import BaseModel
from typing import List


class ReviewResponseModel(BaseModel):
    project: projects.Project
    review: users.Review


class ReviewPaginatedResponse(BaseModel):
    size: int
    results: List[users.Review]

