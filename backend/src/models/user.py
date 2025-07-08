from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.models.base_response import BaseResponse


class UserData(BaseModel):
    id: UUID
    name: str
    mail: str
    avatar: Optional[str]
    created_at: datetime


class UserRequest(BaseModel):
    user_id: UUID


class UserResponse(BaseResponse):
    data: UserData


class UpdateAvatarRequest(UserRequest):
    avatar: str