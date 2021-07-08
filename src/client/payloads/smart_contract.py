from pydantic import BaseModel
from typing import List


class CreateSCProject(BaseModel):
    ownerPrivateKey: str
    reviewerPrivateKey: str
    stagesCost: List[float]


class FundSCProject(BaseModel):
    funderPrivateKey: str
    amount: float


class AcceptSCProjectStage(BaseModel):
    reviewerPrivateKey: str
    completedStage: int

