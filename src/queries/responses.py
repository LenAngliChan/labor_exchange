from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Response, User


async def get_by_id(session: AsyncSession, r_id: int, u_id: int) -> Response:
    query = select(Response).where(id=r_id, user_id=u_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_by_userid(session: AsyncSession, u_id: int) -> Response:
    query = select(Response).filter_by(user_id=u_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_all(u_id: int, session: AsyncSession, limit: int = 100, skip: int = 0) -> list[Response]:
    query = select(Response).where(user_id=u_id).limit(limit).offset(skip)
    result = await session.execute(query)
    return result.scalars().all()


async def create(session: AsyncSession, client: User, vacation_id: int, msg: str) -> Response:
    response = Response(user_id = client.id, job_id = vacation_id, message = msg)
    session.add(response)
    await session.commit()
    await session.refresh(response)
    return response
