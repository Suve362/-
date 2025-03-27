from sqlalchemy import asc, desc, func, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.wallet.models import Wallet
from src.wallet.schemas import WalletCreate
from src.wallet.utils import get_wallet_info


async def get_wallets(
        session: AsyncSession,
        limit: int,
        offset: int,
        sort_by: str | None = "created_at",
        sort_order: str | None = "asc",
) -> tuple[list[Wallet], int]:
    sort_fields = {
        "created_at": Wallet.created_at,
        "updated_at": Wallet.updated_at,
        "id": Wallet.id,
        "balance": Wallet.balance,
    }

    sort_field = sort_fields.get(sort_by, Wallet.created_at)
    order_by = asc(sort_field) if sort_order == "asc" else desc(sort_field)

    stmt = (
        select(Wallet)
        .order_by(order_by)
        .limit(limit)
        .offset(offset)
    )

    result: Result = await session.execute(stmt)
    wallets = result.scalars().all()

    total_stmt = select(func.count(Wallet.id))
    total_result: Result = await session.execute(total_stmt)
    total = total_result.scalar()

    return list(wallets), total


async def create_wallet(session: AsyncSession, wallet_in: WalletCreate) -> Wallet:
    wallet_info = get_wallet_info(wallet_in.wallet_address)
    wallet = Wallet(
        wallet_address=wallet_in.wallet_address,
        balance=wallet_info["balance"],
        bandwidth=wallet_info["bandwidth"],
        energy=wallet_info["energy"],
    )
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    return wallet
