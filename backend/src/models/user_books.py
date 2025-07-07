from pydantic import BaseModel
from src.models.base_response import BaseResponse
from src.models.user import UserRequest
from typing import Optional, List, Literal
from uuid import UUID
from datetime import datetime


class UserBookData(BaseModel):
    user_id: UUID
    book_id: UUID
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    status: str = Literal['want to read', 'reading now', 'have read']


class UserBookRequest(BaseModel):
    user_id: UUID
    status: str = Literal['want to read', 'reading now', 'have read']


class UserBookResponse(BaseResponse):
    data: Optional[List[UserBookData]] = []