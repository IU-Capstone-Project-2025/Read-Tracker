from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from models.base_response import BaseResponse


class UserData(BaseModel):
    id: UUID
    name: str
    mail: str
    avatar: Optional[str]


class UserRequest(BaseModel):
    user_id: UUID


class UserResponse(BaseResponse):
    data: UserData


class UpdateAvatarRequest(UserRequest):
    avatar: str