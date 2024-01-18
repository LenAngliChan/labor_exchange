from settings import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()