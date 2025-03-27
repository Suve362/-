from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import db_helper
from src.wallet import crud
from src.wallet.schemas import (
    WalletCreate,
    WalletPaginatedResponse,
    WalletRead,
    FilterParams,
)

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get(
    "/",
    response_model=WalletPaginatedResponse,
    summary="GET Wallet endpoint for app",
    description="Get few wallets",
)
async def get_wallets(
        filter_query: Annotated[FilterParams, Query()],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    wallets_, total = await crud.get_wallets(
        session=session,
        limit=filter_query.limit,
        offset=filter_query.offset,
        sort_by=filter_query.sort_by,
        sort_order=filter_query.sort_order,
    )
    wallets = [WalletRead.model_validate(wallet) for wallet in wallets_]

    return WalletPaginatedResponse(
        wallets=wallets,
        total=total,
        limit=filter_query.limit,
        offset=filter_query.offset,
    )


@router.post(
    "/",
    response_model=WalletCreate,
    status_code=201,
    summary="POST Wallet endpoint for app",
    description="Create wallet",
)
async def create_wallet(
        wallet_in: WalletCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_wallet(wallet_in=wallet_in, session=session)
