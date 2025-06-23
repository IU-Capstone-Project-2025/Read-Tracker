from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List
from base_response import BaseResponse


class NoteData:
    id: UUID
    text: str
    book_id: UUID
    created_at: datetime


class NoteRequest:
    text: str


class NoteResponse(BaseResponse):
    data: List[NoteData]
