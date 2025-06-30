from fastapi import APIRouter, HTTPException
from models.reviews import ReviewRequest, ReviewResponse, ReviewData
from models.base_response import BaseResponse
from models.user import UserRequest
from database.db_instance import db_handler
from uuid import UUID

router = APIRouter(tags=["Reviews"])


@router.get("/me/reviews", response_model=ReviewResponse, status_code=200)
async def get_reviews(request: UserRequest):
    data, err = db_handler.getReview(user_id=request.user_id)
    answer = []
    if data:
        for review in data:
            answer.append(ReviewData(
                rate=review.rate,
                text=review.text,
                book_id=review.book_id,
                user_id=review.user_id,
                created_at=review.created_at
            ))
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": answer
    }


@router.get("/reviews/{book_id}", response_model=ReviewResponse, status_code=200)
async def get_review(request: UserRequest, book_id: UUID):
    data, err = db_handler.getReview(user_id=request.user_id, book_id=book_id)
    answer = []
    if data:
        for review in data:
            answer.append(ReviewData(
                rate=review.rate,
                text=review.text,
                book_id=review.book_id,
                user_id=review.user_id,
                created_at=review.created_at
            ))
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": answer
    }


@router.put("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def update_review(request: ReviewRequest, book_id: UUID):
    if not book_id:
        raise HTTPException(status_code=404, detail="Book id not found")
    err = db_handler.updateReview(user_id=request.user_id, book_id=book_id, text=request.text, rate=request.rate)
    return {
        "status": "success",
        "message": "Review updated"
    }


@router.delete("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def delete_review(request: UserRequest, book_id: UUID):
    if not book_id:
        raise HTTPException(status_code=404, detail="Book id not found")
    err = db_handler.deleteReview(user_id=request.user_id book_id=book_id)
    return {
        "status": "success",
        "message": "Review deleted"
    }


@router.post("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def create_review(request: ReviewRequest, book_id: UUID):
    if not book_id:
        raise HTTPException(status_code=404, detail="Book id not found")
    err = db_handler.addReview(user_id=request.user_id, book_id=book_id, rate=request.rate, text=request.text)
    return {
        "status": "success",
        "message": "Review created"
    }
