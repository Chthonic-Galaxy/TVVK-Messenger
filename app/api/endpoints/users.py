from fastapi import APIRouter, Depends

from app.schemas import user as user_schema
from app.api.deps import CurrentUser

router = APIRouter()

@router.get("/me", response_model=user_schema.UserRead)
async def read_user_me(current_user: CurrentUser):
    return current_user
