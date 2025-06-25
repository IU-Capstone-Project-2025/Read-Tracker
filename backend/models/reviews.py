from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from base_response import BaseResponse
from typing import List


class ReviewRequest(BaseModel):
    rate: int = Field(ge=1, le=10)
    text: str


class ReviewData:
    user_id: UUID
    book_id: UUID
    rate: int = Field(ge=1, le=10)
    text: str
    created_at: datetime


class ReviewResponse(BaseResponse):
    data: List[ReviewData]