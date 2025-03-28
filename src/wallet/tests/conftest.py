import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database import Base, DatabaseHelper

test_engine = create_async_engine(settings.DB_URL, poolclass=NullPool, echo=False)
test_db_helper = DatabaseHelper(url=settings.DB_URL)
test_db_helper.engine = test_engine
test_db_helper.session_factory = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with test_db_helper.session_factory() as session:
        async with test_db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session
        async with test_db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
