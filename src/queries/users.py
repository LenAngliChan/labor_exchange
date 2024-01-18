from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from schemas import UserCreateSchema
from core import hash_password


# TODO: get_by
async def get_by_email(session: AsyncSession, u_email: str) -> User:
    query = select(User).filter_by(email=u_email).limit(1)
    result = await session.execute(query)
    return result.scalars().first()


# TODO: Отступы
async def get_by_id(session: AsyncSession, u_id: int) -> User:
    result = await session.get(User, u_id)
    return result


async def get_all(session: AsyncSession, limit: int = 100, skip: int = 0) -> list[User]:
    query = select(User).limit(limit).offset(skip)
    result = await session.execute(query)
    return result.scalars().all()


async def create(session: AsyncSession, client: UserCreateSchema) -> User:
    print(client)
    user = User(name = client.name, hashed_password = hash_password(client.password), email = client.email, is_company = client.is_company)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# TODO: ответственность БД
async def update(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
