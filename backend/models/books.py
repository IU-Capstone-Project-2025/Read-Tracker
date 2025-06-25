from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from models.base_response import BaseResponse


class BookData(BaseModel):
    id: UUID
    author: str
    title: str
    language: str
    description: str
    cover: str


class BookResponse(BaseResponse):
    data: Optional[List[BookData]] = []