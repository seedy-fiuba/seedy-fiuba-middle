from pydantic import BaseModel
from ...models.projects import Status


class UpdateProjectPayload(BaseModel):
    status: Status = None
    currentStageId: int = None
    walletId: int = None
    reviewerId: int = None

