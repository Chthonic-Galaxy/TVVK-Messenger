from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, get_async_session
from app.schemas import contact as contact_schema
from app.db import models as user_model
from app.db import models as contact_model

router = APIRouter()

@router.post("/", response_model=contact_schema.ContactRead, status_code=HTTP_201_CREATED)
async def create_contact(
    contact_in: contact_schema.ContactCreate,
    current_user: CurrentUser,
    session: AsyncSession = Depends(get_async_session)
):
    if contact_in.username == current_user.username:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="You cannot add yourself to contact list"
        )
    contact_user = await session.scalar(
        select(user_model.User).where(user_model.User.username == contact_in.username)
    )
    if not contact_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Contact user not found"
        )
    
    contact = await session.scalar(
        select(contact_model.Contact).where(
            contact_model.Contact.user_id == current_user.id,
            contact_model.Contact.contact_id == contact_user.id
        )
    )
    if contact:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="This user already in your contact list"
        )
    
    contact = contact_model.Contact(
        user_id=current_user.id,
        contact_id=contact_user.id
    )
    
    result = contact_schema.ContactRead(
        id=0,
        contact_id=0,
        username=contact_user.username,
        nickname=contact_user.nickname
    )
    
    session.add(contact)
    await session.commit()
    await session.refresh(contact)

    result.id, result.contact_id = contact.id, contact.contact_id

    return result

@router.get("/me", response_model=list[contact_schema.ContactRead])
async def read_contacts(
    current_user: CurrentUser,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(
        contact_model.Contact.id,
        contact_model.Contact.contact_id,
        user_model.User.username,
        user_model.User.nickname
    ).join(
        user_model.User, contact_model.Contact.contact_id == user_model.User.id
    ).where(contact_model.Contact.user_id == current_user.id)
    
    result = await session.execute(stmt)
    contacts = []
    for row in result:
        contacts.append(contact_schema.ContactRead(
            id=row.id,
            contact_id=row.contact_id,
            username=row.username,
            nickname=row.nickname
        ))

    return contacts
