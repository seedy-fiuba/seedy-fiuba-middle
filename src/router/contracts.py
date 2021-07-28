from fastapi import APIRouter, Depends
from src.responses import ContractProjectSearchResponse
from ..controller import contracts_controller
from typing import Optional


router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)


@router.get('', response_model=ContractProjectSearchResponse)
async def get_contracts(funderId: Optional[str] = None, size: Optional[str] = None, page: Optional[str] = None):
    return await contracts_controller.get_contracts(funderId, size, page)
