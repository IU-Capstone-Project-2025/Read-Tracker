from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# TODO: Replace mockup
@router.get("/", status_code=200)
async def get_reviews():
    return JSONResponse(content={
        "status": "success",
        "message": "Reviews retrieved",
        "data": []  # Array of books (may be empty if no books)
    })


# TODO: Replace mockup, 404 error
@router.get("/{review_id}", status_code=200)
async def get_review(review_id: int):
    if review_id:
        pass

    return JSONResponse(content={
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
    })


# TODO: Replace mockup; Code validation steps, 400, 404 errors
@router.post("/", status_code=200)
async def add_review(request: Request):
    if request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Review created",
        "data": []
    })


# TODO: Replace mockup; Code validation steps, 400, 404 errors.
@router.put("/{review_id}", status_code=200)
async def update_review(request: Request, review_id: int):
    if request or review_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Review updated",

    })


# TODO: Replace mockup; 404 error.
@router.delete("/{review_id}", status_code=200)
async def delete_book(review_id: int):
    if review_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Review deleted",
    })
