from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

def create_engine(dns: str) -> AsyncEngine:
    return create_async_engine(dns, pool_pre_ping=True, pool_size=10, max_overflow=20)

def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)