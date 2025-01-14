from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.db import models as user_model
from app.db.session import get_async_session
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=user_schema.UserRead, status_code=HTTP_201_CREATED)
async def register_user(user_in: user_schema.UserCreate, session: AsyncSession = Depends(get_async_session)):
    db_user = await session.scalar(
        select(user_model.User).where(user_model.User.email == user_in.email)
    )
    if db_user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    
    db_user_username  = await session.scalar(
        select(user_model.User).where(user_model.User.username == user_in.username)
    )
    if db_user_username:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    
    hashed_password = get_password_hash(user_in.password)
    db_user = user_model.User(
        email=user_in.email,
        hashed_password=hashed_password,
        username=user_in.username,
        nickname=user_in.nickname
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@router.post("/login", response_model=token_schema.Token)
async def login_access_token(form_data: user_schema.UserLogin, session: AsyncSession = Depends(get_async_session)):
    user = await session.scalar(
        select(user_model.User).where(user_model.User.email == form_data.email)
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    access_token = create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}
