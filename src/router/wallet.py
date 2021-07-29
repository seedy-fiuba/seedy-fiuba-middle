from fastapi import APIRouter, status as HTTPStatus, Depends
from ..controller import wallet_controller
from ..dependencies import get_token_header
from ..responses import WalletBalanceResponse
from ..payloads import TransferFundsPayload
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
    dependencies=[Depends(get_token_header)]
)


@router.get('/{user_id}', response_model=WalletBalanceResponse, tags=['wallet'])
async def get_wallet_balance(user_id: int):
    return await wallet_controller.get_balance(user_id)


@router.post('/{user_id}/transfer', status_code=HTTPStatus.HTTP_204_NO_CONTENT, response_class=PlainTextResponse,
          tags=['wallet'])
async def transfer_funds(user_id: int, payload: TransferFundsPayload):
    return await wallet_controller.transfer_funds(user_id, payload)