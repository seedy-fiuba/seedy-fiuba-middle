from pydantic import BaseModel
from ...models.projects import Status


class UpdateProjectPayload(BaseModel):
    title: str = None
    category: str = None
    description: str = None
    status: Status = None
    currentStageId: int = None
    walletId: int = None
    reviewerId: int = None
    missingAmount: float = None


class FundProjectClientPayload(BaseModel):
    funderId: int = None
    currentFundedAmount: float = None
    txHash: str = None

