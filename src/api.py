from fastapi import APIRouter
from src.wallet.views import router as wallet_router


api_router = APIRouter()
api_router.include_router(wallet_router)
