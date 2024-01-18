from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from core.config import STAGE

DB_USER = os.environ.get("DB_USER", "admin")
DB_PASS = os.environ.get("DB_PASS", "admin")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "labor-exchange")

if STAGE == 'memory':
    DB_URL = "postgresql+asyncpg:///:memory:"
else:
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(DB_URL, echo=True)
Base = declarative_base()
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                           bind=engine, class_=AsyncSession))


# TODO: скоммуниздить инициализацию из репо

async def db_init():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    return
