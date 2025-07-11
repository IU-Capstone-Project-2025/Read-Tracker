from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.models.base_response import BaseResponse


class NoteData(BaseModel):
    id: UUID
    text: Optional[str]
    book_id: UUID
    user_id: UUID
    created_at: datetime


class NoteRequest(BaseModel):
    user_id: UUID
    text: Optional[str]


class NoteResponse(BaseResponse):
    data: Optional[List[NoteData]] = []
