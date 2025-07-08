from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.models.base_response import BaseResponse
from datetime import date


class TrackerRequest(BaseModel):
    user_id: UUID


class TrackerData(BaseModel):
    id: int
    user_id: UUID
    start_date: datetime
    end_date: Optional[date]
    last_marked: datetime


class TrackerResponse(BaseResponse):
    data: Optional[List[TrackerData]] = []