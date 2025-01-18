from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    nickname: Optional[Annotated[str, StringConstraints(max_length=50)]] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    nickname: Optional[str] = None

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    nickname: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints()]

class SearchUsersResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    in_contacts: list[UserPublic]
    users: list[UserPublic]
