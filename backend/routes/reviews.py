from uuid import uuid4, UUID

from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from starlette import status
from backend.models.reviews import NewReviewRequest, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["review"])

# TODO: implement code
@router.get("/", response_model=dict)
async def get_reviews():
    data = repository.getReviews()
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": data
    }


@router.get("/{review_id}", response_model=dict)
async def get_review(review_id: UUID):
    data, error = repository.getReview(review_id)
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Review not found"}
        )
    return {
        "status": "success",
        "message": "Review retrieved",
        "data": data
    }


@router.post("/reviews", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_review(review_request: NewReviewRequest):
    error = repository.checkBookExist(review_request.book_id)
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Book not found"}
        )

    # TODO: validate
    try:
        review_id = uuid4()
        user_id = uuid4()

        review_data = ReviewResponse(
            id=review_id,
            user_id=user_id,
            **review_request.dict()
        )

        # TODO: put in bd

        return {
            "status": "success",
            "message": "Review created",
            "data": {"id": str(review_id)}
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )


### ВСЕ ЧТО ДАЛЬШЕ ЕЩЕ НЕ ПРИВЕДЕНО В АДЕКВАТ ОТ НЕЙРОНКИ
@router.put("/reviews/{review_id}", response_model=dict)
async def update_review(review_id: UUID, review_update: ReviewUpdate):
    if review_id not in reviews_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Review not found"}
        )

    current_review = reviews_db[review_id]

    try:
        update_data = review_update.dict(exclude_unset=True)

        # Проверка существования книги, если book_id в update_data
        if 'book_id' in update_data and update_data['book_id'] not in books_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Book not found"}
            )

        # Обновляем данные
        for field, value in update_data.items():
            current_review[field] = value

        reviews_db[review_id] = current_review

        return {
            "status": "success",
            "message": "Review changed"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )

@router.delete("/reviews/{review_id}", response_model=dict)
async def delete_review(review_id: UUID):
    if review_id not in reviews_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Review not found"}
        )

    del reviews_db[review_id]

    return {
        "status": "success",
        "message": "Review deleted"
    }