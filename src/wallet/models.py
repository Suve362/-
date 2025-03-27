import uuid
from sqlalchemy import UUID, Boolean, String, Float, Integer, func, text

from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.mixins import TimeStampMixin


class Wallet(TimeStampMixin, Base):
    """Wallet model"""

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    wallet_address: Mapped[str] = mapped_column(String(255), unique=True)
    balance: Mapped[float] = mapped_column(Float, )
    bandwidth: Mapped[int] = mapped_column(Integer)
    energy: Mapped[int] = mapped_column(Integer)
