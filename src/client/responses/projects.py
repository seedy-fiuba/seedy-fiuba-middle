from ...models import projects
from pydantic import BaseModel
from typing import List


class ContractPaginatedResponse(BaseModel):
    totalItems: int = None
    contracts: List[projects.Contract] = []
    totalPages: int
    currentPage: int