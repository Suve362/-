import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron
from tronpy.keys import is_base58check_address

from src.wallet.crud import create_wallet
from src.wallet.schemas import WalletCreate

client = Tron(network="nile")

@pytest.mark.asyncio
async def test_wallet_creation(session: AsyncSession):
    wallet_address = client.generate_address()["base58check_address"]
    assert is_base58check_address(wallet_address), "Generated address is invalid"
    wallet_data = WalletCreate(wallet_address=wallet_address)
    wallet = await create_wallet(session, wallet_data)

    assert isinstance(wallet_address, str)
    assert isinstance(wallet.balance, (int, float))
    assert isinstance(wallet.bandwidth, int)
    assert isinstance(wallet.energy, int)

    assert wallet.wallet_address == wallet_address
    assert wallet.balance >= 0
    assert wallet.bandwidth is not None
    assert wallet.energy is not None

