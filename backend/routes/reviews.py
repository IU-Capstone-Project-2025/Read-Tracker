from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..models.reviews import ReviewRequest, ReviewResponse
from ..models.base_response import BaseResponse

router = APIRouter(tags=["Reviews"])


# TODO: Replace mockup
@router.get("/reviews/{book_id}", response_model=ReviewResponse, status_code=200)
async def get_reviews(book_id: int):
    if book_id:
        pass
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": []
    }


# TODO: Replace mockup
@router.get("/me/reviews", response_model=ReviewResponse, status_code=200)
async def get_review():
    return {
        "status": "success",
        "message": "Review retrieved",
        "data": {
            "id": "uuid",
            "content_type": "good_review",
            "user_id": 123,
            "rate": 5,
            "text": "Great read!",
            "book_id": 123
        }
    }


# TODO: Replace mockup
@router.put("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def update_review(book_id: int):
    if book_id:
        pass
    return {
        "status": "success",
        "message": "Review updated"
    }


# TODO: Replace mockup
@router.delete("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def delete_review(review_id: int):
    if review_id:
        pass
    return {
        "status": "success",
        "message": "Review deleted"
    }


# TODO: Replace mockup
@router.post("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def create_review(review_id: int):
    if review_id:
        pass
    return {
        "status": "success",
        "message": "Review created"
    }
