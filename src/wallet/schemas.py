from datetime import datetime, timezone
from pydantic import UUID4, BaseModel, ConfigDict, Field, HttpUrl


class WalletBase(BaseModel):
    """Base User model"""

    pass


class WalletRead(WalletBase):
    """Wallet read model"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    wallet_address: str
    balance: float = Field(..., gt=0)
    bandwidth: int | None
    energy: int | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WalletCreate(WalletBase):
    """Create Wallet"""

    wallet_address: str


class WalletPaginatedResponse(BaseModel):
    wallets: list[WalletRead]
    total: int
    limit: int
    offset: int


class FilterParams(BaseModel):
    limit: int = Field(default=10, ge=0, le=20, description="Limit")
    offset: int = Field(default=0, ge=0, description="Offset")
    sort_by: str = Field(
        default="created_at",
        description="Field to sort by (created_at, updated_at, id, balance)",
    )

    sort_order: str = Field(default="asc", description="Sort order (asc, desc)")
