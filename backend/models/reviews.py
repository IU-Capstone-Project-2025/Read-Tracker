from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID, uuid4

class NewReviewRequest(BaseModel):
    book_id: UUID
    rate: int = Field(..., ge=1, le=5)
    text: str

    @validator('text')
    def validate_text(cls, v):
        if len(v) < 5:
            raise ValueError("Text must be at least 5 characters long")
        if len(v) > 1000:
            raise ValueError("Text must be less than 1000 characters")
        return v

class ReviewResponse(NewReviewRequest):
    id: UUID
    user_id: UUID


class ReviewUpdateRequest(BaseModel):
    rate: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None

    @validator('text')
    def validate_text(cls, v):
        if v is not None:
            if len(v) < 5:
                raise ValueError("Text must be at least 5 characters long")
            if len(v) > 1000:
                raise ValueError("Text must be less than 1000 characters")
        return v