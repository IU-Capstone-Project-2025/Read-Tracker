from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from src.models.base_response import BaseResponse


class TagData(BaseModel):
    id: UUID
    name: str
    description: Optional[str]


class BookData(BaseModel):
    id: UUID
    author: Optional[str]
    title: str
    language: Optional[str]
    description: Optional[str]
    cover: Optional[str]
    tags: Optional[List[TagData]] = []


class BookResponse(BaseResponse):
    data: Optional[List[BookData]] = []