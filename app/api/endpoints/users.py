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
    in_contact_query = (
        select(user_model.User).options(load_only(user_model.User.username, user_model.User.nickname))
        .join(contact_model.Contact, contact_model.Contact.contact_id == user_model.User.id)
        .where(contact_model.Contact.user_id == current_user.id)
    )
    
    users_query = select(user_model.User).options(load_only(user_model.User.username, user_model.User.nickname))
    
    if search:
        in_contact_query = in_contact_query.where(
            or_(
                user_model.User.username.icontains(search),
                user_model.User.nickname.icontains(search),
            )
        )
        users_query = users_query.where(
            or_(
                user_model.User.username.icontains(search),
                user_model.User.nickname.icontains(search),
            )
        )
    
    in_contacts_users = (await session.scalars(in_contact_query.limit(limit).offset(offset))).all()
    
    users_not_in_contacts = (await session.scalars(
        users_query.filter(user_model.User.id.not_in([user.id for user in in_contacts_users])).limit(limit).offset(offset)
    )).all()
    print({"in_contacts": in_contacts_users, "users": users_not_in_contacts})
    
    return {"in_contacts": in_contacts_users, "users": users_not_in_contacts}
    