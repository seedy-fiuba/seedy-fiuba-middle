from pydantic import BaseModel
from typing import List


class CreateSCProject(BaseModel):
    ownerPrivateKey: str
    reviewerPrivateKey: str
    stagesCost: List[float]
