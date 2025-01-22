from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from starlette.status import HTTP_404_NOT_FOUND

from app.schemas import user as user_schema
from app.db import models as user_model
from app.db import models as contact_model
from app.db.session import get_async_session
from app.api.deps import CurrentUser

router = APIRouter()

@router.get("/me", response_model=user_schema.UserRead)
async def read_user_me(current_user: CurrentUser):
    return current_user

@router.get("/", response_model=user_schema.SearchUsersResult)
async def search_users(
    current_user: CurrentUser,
    search: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(user_model.User)
    
    if search:
        query = query.where(
            or_(
                user_model.User.username.icontains(search),
                user_model.User.nickname.icontains(search),
            )
        )
    
    users = (await session.scalars(query.limit(limit).offset(offset))).all()
    return {"users": users}
    