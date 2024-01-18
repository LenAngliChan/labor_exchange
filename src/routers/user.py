from fastapi import APIRouter, Depends
from starlette.responses import Response
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from core import hash_password
from schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from queries import users as user_queries
from dependencies import get_session, get_current_user
from models import User
from core.exceptions import client_exception, access_exception

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def read_user(current_user: User = Depends(get_current_user)):
    return UserSchema.model_validate(current_user)


@router.get("/{id}", response_model=UserSchema)
async def read_user(id: int, session: AsyncSession = Depends(get_session)):
    db_user = await user_queries.get_by_id(session = session, u_id = id)
    if db_user is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return UserSchema.model_validate(db_user)


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    db_user = await user_queries.create(session = session, client = user)
    return UserSchema.model_validate(db_user)


@router.put("/{id}", response_model=UserSchema)
async def update_user(id: int, user: UserUpdateSchema, session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user)):
    db_user = await user_queries.get_by_id(session = session, u_id = id)

    if db_user is None:
        raise client_exception
    if db_user.email != current_user.email:
        raise access_exception

    db_user.name = user.name
    db_user.is_company = user.is_company
    db_user.hashed_password = hash_password(user.password)

    db_user = await user_queries.update(session = session, user = db_user)
    return UserSchema.model_validate(db_user)
