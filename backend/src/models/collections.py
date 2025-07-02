from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class CollectionRequest(BaseModel):
    title: str
    description: Optional[str] = None
    is_private: bool = False
    cover: Optional[HttpUrl] = None


class CollectionData(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    cover: Optional[str]
    is_private: bool
    created_at: datetime
    user_id: UUID


class CollectionResponse(BaseModel):
    status: str
    message: str
    data: List[CollectionData]

class AddBookToCollectionRequest(BaseModel):
    book_id: UUID