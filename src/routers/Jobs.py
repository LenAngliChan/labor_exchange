from functools import wraps

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from schemas import JobSchema, JobUpdateSchema, JobCreateSchema
from queries import jobs as job_queries
from dependencies import get_session, get_current_user
from models import User
from core.exceptions import companies_exception, job_exception, access_exception
from starlette import status

router = APIRouter(prefix="/jobs", tags=["jobs"])


def only_companies(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs['current_user']
        if not user.is_company:
            raise companies_exception
        return await func(*args, **kwargs)
    return wrapper


@router.get("/", response_model=list[JobSchema])
async def read_jobs(limit: int = 100, skip: int = 0, session: AsyncSession = Depends(get_session)):
    result = await job_queries.get_all(session = session, limit = limit, skip = skip)
    return [JobSchema.model_validate(db_job) for db_job in result]


@router.get("/{id}", response_model=JobSchema)
async def read_job(id: int, session: AsyncSession = Depends(get_session)):
    db_job = await job_queries.get_by_id(session = session, j_id = id)
    if db_job is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JobSchema.model_validate(db_job)

# TODO: magic const
# TODO: отступы


@router.post("/", response_model=JobSchema)
@only_companies
async def create_job(job: JobCreateSchema, current_user: User = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):
    db_job = await job_queries.create(session = session, client = current_user, vacation = job)
    return JobSchema.model_validate(db_job)


@router.put("/{id}", response_model=JobSchema)
@only_companies
async def update_job(id: int, job: JobUpdateSchema, current_user: User = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):
    db_job = await job_queries.get_by_id(session = session, j_id = id)

    if db_job is None:
        raise job_exception
    elif db_job.user_id != current_user.id:
        raise access_exception

    db_job.title = job.title
    db_job.description = job.description
    db_job.is_active = job.is_active
    db_job.salary_from = job.salary_from
    db_job.salary_to = job.salary_to

    updated_job = await job_queries.update(session = session, job = db_job)
    return JobSchema.model_validate(updated_job)


@router.delete("/{id}", response_model=bool)
@only_companies
async def delete_job(id: int, current_user: User = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):
    db_job = await job_queries.get_by_id(session=session, j_id=id)

    if db_job is None:
        raise job_exception
    elif db_job.user_id != current_user.id:
        raise access_exception

    return await job_queries.delete(session = session, job = db_job)
