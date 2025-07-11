from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from src.models.books import BookData


class CollectionRequest(BaseModel):
    title: str
    description: Optional[str] = None
    is_private: bool = False
    cover: Optional[HttpUrl] = None


class CollectionRequestWithUserID(CollectionRequest):
    user_id: UUID


class CollectionData(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    cover: Optional[str]
    is_private: bool
    created_at: datetime
    items: Optional[List[BookData]] = []


class CollectionResponse(BaseModel):
    status: str
    message: str
    data: List[CollectionData]


class AddBookToCollectionRequest(BaseModel):
    book_id: UUID
