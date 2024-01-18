from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Job
from schemas import UserSchema, JobCreateSchema

async def get_by_id(session: AsyncSession, j_id: int) -> Job:
    query = select(Job).filter_by(id = j_id)
    result = await session.execute(query)
    return result.scalars().first()

async def get_all(session: AsyncSession, limit: int = 100, skip: int = 0) -> list[Job]:
    query = select(Job).limit(limit).offset(skip)
    result = await session.execute(query)
    return result.scalars().all()

async def create(session: AsyncSession, client: UserSchema, vacation: JobCreateSchema):
    job = Job(user_id = client.id, title = vacation.title, description = vacation.description, salary_from = vacation.salary_from,
              salary_to = vacation.salary_to, is_active = vacation.is_active)
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job

async def update(session: AsyncSession, job: Job) -> Job:
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job

async def delete(session: AsyncSession, job: Job) -> bool:
    await session.delete(job)
    await session.commit()
    #await session.refresh(job)
    return True