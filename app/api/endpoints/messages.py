from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.api.deps import CurrentUser
from app.schemas import message as message_schema
from app.db import models as user_model
from app.db import models as message_model
from app.db.session import get_async_session
from app.core.security.asymmetric_encryption import encrypt_message

router = APIRouter()

@router.post("/", response_model=message_schema.MessageRead, status_code=HTTP_201_CREATED)
async def send_personal_message(
    message_in: message_schema.MessageCreate,
    current_user: CurrentUser,
    session: AsyncSession = Depends(get_async_session)
):
    recipient = await session.scalar(
        select(user_model.User).where(user_model.User.username == message_in.recipient_username)
    )
    if not recipient:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipient not found")
    
    if not recipient.public_key:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Recipient has no public key")
    
    sender = current_user
    if not sender.public_key:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Recipient has no public key")
    
    encrypted_content_recipient = encrypt_message(message_in.content, recipient.public_key)
    encrypted_content_sender = encrypt_message(message_in.content, sender.public_key)
    
    message = message_model.Message(
        sender_id=current_user.id,
        recipient_id=recipient.id,
        encrypted_content_recipient=encrypted_content_recipient,
        encrypted_content_sender=encrypted_content_sender
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    
    return message_schema.MessageRead(
        id=message.id,
        sender_username=current_user.username,
        content="Message encrypted",
        timestamp=message.timestamp
    )

@router.get("/me", response_model=list[message_schema.MessageRead])
async def read_personal_messages(
    current_user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=100)
):
    messages = await session.scalars(
        select(message_model.Message)
        .options()
        .where(
            or_(
                message_model.Message.sender_id == current_user.id,
                message_model.Message.recipient_id == current_user.id,
            )
        )
        .order_by(message_model.Message.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    message_list = []
    for message in messages:
        sender_username_db = await session.scalar(select(user_model.User.username).where(user_model.User.id == message.sender_id))
        recipient_username_db = await session.scalar(select(user_model.User.username).where(user_model.User.id == message.recipient_id))
        if current_user.id == message.sender_id:
            content_to_display = "Message encrypted (for you)"
        elif current_user.id == message.recipient_id:
            content_to_display = "Message encrypted (for recipient)"
        else:
            content_to_display = "Message encrypted"
        message_list.append(message_schema.MessageRead(
            id = message.id,
            sender_username=sender_username_db,
            content=content_to_display,
            timestamp=message.timestamp
        ))
    return message_list
