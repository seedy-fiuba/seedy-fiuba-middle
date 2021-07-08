from src.exceptions import MiddleException
from ..client import users as users_client, smart_contract as sc_client


async def get_balance(user_id: int):
    # Get user private key
    user = await users_client.get_user(user_id)

    if user.walletPrivateKey is None:
        raise MiddleException(status=400, detail={'error': 'User does not have a wallet', 'status': 400})

    # Get wallet balance from smart contract
    return await sc_client.get_balance(user.walletPrivateKey)

