from typing import List
from pydantic import BaseModel
from uuid import UUID

from src.models.reviews import ReviewData


class SubscribeRequest(BaseModel):
    publisher_id: UUID
    subscriber_id: UUID


class SubscriptionReviewsResponse(BaseModel):
    data: List[ReviewData]


class SubscriptionReviewsRequest(BaseModel):
    subscriber_id: UUID
