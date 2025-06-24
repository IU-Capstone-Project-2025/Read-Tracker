from pydantic import BaseModel
from datetime import datetime


class TrackerRequest(BaseModel):
    date: datetime
