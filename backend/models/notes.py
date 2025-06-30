from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from models.base_response import BaseResponse
from models.user import UserRequest

class NoteData(BaseModel):
    id: UUID
    text: Optional[str]
    book_id: UUID
    user_id: UUID
    created_at: datetime


class NoteRequest(UserRequest):
    text: Optional[str]


class NoteResponse(BaseResponse):
    data: Optional[List[NoteData]] = []
