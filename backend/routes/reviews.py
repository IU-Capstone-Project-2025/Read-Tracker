from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from models.reviews import ReviewRequest, ReviewResponse, ReviewData
from models.base_response import BaseResponse
from database.db_instance import db_handler
from uuid import UUID

router = APIRouter(tags=["Reviews"])


# TODO: Replace mockup
@router.get("/me/reviews", response_model=ReviewResponse, status_code=200)
async def get_reviews():
    data, err = db_handler.getReview()
    answer = []
    if data:
        for review in data:
            answer.append(ReviewData(rate=review.rate,
                                     text=review.text,
                                     book_id=review.book_ID,
                                     user_id=review.user_ID,
                                     created_at=review.created_at))
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": answer
    }


# TODO: Replace mockup
@router.get("/reviews/{book_id}", response_model=ReviewResponse, status_code=200)
async def get_review(book_id: UUID):
    data, err = db_handler.getReview(book_id=book_id)
    answer = []
    if data:
        for review in data:
            answer.append(ReviewData(rate=review.rate,
                                     text=review.text,
                                     book_id=review.book_ID,
                                     user_id=review.user_ID,
                                     created_at=review.created_at))
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": answer
    }


# TODO: Replace mockup
@router.put("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def update_review(request: ReviewRequest, book_id: UUID):
    if book_id:
        pass
    err = db_handler.updateReview(book_id=book_id, text=request.text, rate=request.rate)
    return {
        "status": "success",
        "message": "Review updated"
    }


# TODO: Replace mockup
@router.delete("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def delete_review(book_id: UUID):
    if book_id:
        pass
    err = db_handler.deleteReview(book_id=book_id)
    return {
        "status": "success",
        "message": "Review deleted"
    }


# TODO: Replace mockup
@router.post("/me/reviews/{book_id}", response_model=BaseResponse, status_code=200)
async def create_review(request: ReviewRequest, book_id: UUID):
    if book_id:
        pass
    err = db_handler.addReview(book_id=book_id, rate=request.rate, text=request.text)
    return {
        "status": "success",
        "message": "Review created"
    }
