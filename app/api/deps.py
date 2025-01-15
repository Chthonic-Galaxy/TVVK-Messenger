from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.db.session import get_async_session
from app.db import models as user_model
from app.schemas import token as token_schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session)
) -> user_model.User:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token,
            key=settings.AUTH_SECRET_KEY,
            algorithms=settings.AUTH_ALGORITHM
        )
        token_data = token_schema.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await session.scalar(
        select(user_model.User).where(user_model.User.username == token_data.sub)
    )
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[user_model.User, Depends(get_current_user)]
