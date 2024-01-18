from functools import wraps
from starlette.responses import Response
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ResponseSchema
from queries import responses as resp_queries
from dependencies import get_session, get_current_user
from models import User
from core.exceptions import applicants_exception

router = APIRouter(prefix="/responses", tags=["responses"])


def only_applicants(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs['current_user']
        if user.is_company:
            raise applicants_exception
        return await func(*args, **kwargs)
    return wrapper


# TODO: Защитить
# TODO: Крайние случаи
@router.get("/", response_model=list[ResponseSchema])
async def read_responses(limit: int = 100, skip: int = 0, current_user: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session)):
    result = await resp_queries.get_all(session=session, limit=limit, skip=skip, u_id=current_user.id)
    return [ResponseSchema.model_validate(db_resp) for db_resp in result]


@router.get("/{id}", response_model=ResponseSchema)
async def read_response(id: int, current_user: User = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session)):
    db_resp = await resp_queries.get_by_id(session=session, r_id=id, u_id=current_user.id)
    if db_resp is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return ResponseSchema.model_validate(db_resp)


@router.post("/", response_model=ResponseSchema)
@only_applicants
async def create_response(job_id: int, msg: str, current_user: User = Depends(get_current_user),
                          session: AsyncSession = Depends(get_session)):
    db_resp = await resp_queries.create(session=session, client=current_user, vacation_id=job_id, msg=msg)
    return ResponseSchema.model_validate(db_resp)
