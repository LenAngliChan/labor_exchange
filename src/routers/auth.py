from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import LoginSchema, TokenSchema
from queries import users as user_queries
from dependencies import get_session
from core import verify_password, create_access_token
from core.exceptions import client_exception, credentials_exception

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", response_model=TokenSchema)
async def login(login: LoginSchema, session: AsyncSession = Depends(get_session)):
    db_user = await user_queries.get_by_email(session = session, u_email = login.email)
    if db_user is None:
        raise client_exception
    if not verify_password(login.password, db_user.hashed_password):
        raise credentials_exception
    return TokenSchema(access_token=create_access_token({"sub": db_user.email}),
                       token_type="Bearer")

