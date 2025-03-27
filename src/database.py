from asyncio import current_task

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from src.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"auth_{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url=url,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session


db_helper = DatabaseHelper(
    url=settings.DB_URL,
)
