from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List
from base_response import BaseResponse


class NoteData(BaseModel):
    id: UUID
    text: str
    book_id: UUID
    created_at: datetime


class NoteRequest(BaseModel):
    text: str


class NoteResponse(BaseResponse):
    data: List[NoteData]
