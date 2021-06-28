from .models import projects, users
from pydantic import BaseModel


class ReviewResponseModel(BaseModel):
    project: projects.Project
    review: users.Review

