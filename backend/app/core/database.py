from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

import asyncpg

async def get_connection():
    return await asyncpg.connect(
        host='aws-1-ap-southeast-2.pooler.supabase.com',
        port=6543,
        user='postgres.sxrqneejcksykpamyjzu',
        password=settings.SUPABASE_PASSWORD,
        database='postgres',
        ssl='require',
        statement_cache_size=0,
    )

def get_engine():
    return create_async_engine(
        settings.SUPABASE_DB_URL,
        pool_pre_ping=True,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
        },
    )

engine = get_engine()

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
