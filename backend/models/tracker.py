from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from models.base_response import BaseResponse


class TrackerRequest(BaseModel):
    date: datetime


class TrackerData(BaseModel):
    id: UUID
    user_id: UUID
    start_date: datetime
    end_date: datetime


class TrackerResponse(BaseResponse):
    data: Optional[List[TrackerData]] = []