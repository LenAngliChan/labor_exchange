from dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.security import JWTBearer, decode_access_token
from models import User
from core.exceptions import credentials_exception
from queries import users as user_queries


async def get_current_user(session: AsyncSession = Depends(get_session),
                           token: str = Depends(JWTBearer())) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    db_email: str = payload.get('sub')
    if db_email is None:
        raise credentials_exception
    db_user = await user_queries.get_by_email(session = session, u_email = db_email)
    if db_user is None:
        raise credentials_exception
    return db_user
