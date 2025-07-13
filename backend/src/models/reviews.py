from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from src.models.base_response import BaseResponse
from typing import List, Optional


class ReviewRequest(BaseModel):
    user_id: UUID
    rate: Optional[int] = Field(ge=1, le=10)
    text: Optional[str]


class ReviewData(BaseModel):
    user_id: UUID
    book_id: UUID
    rate: int = Field(ge=1, le=10)
    text: Optional[str]
    created_at: datetime


class ReviewResponse(BaseResponse):
    data: List[ReviewData]
