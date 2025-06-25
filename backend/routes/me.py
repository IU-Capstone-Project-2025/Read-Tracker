from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from models.base_response import BaseResponse
from models.tracker import TrackerRequest, TrackerResponse, TrackerData
from typing import Optional
from database.db_instance import db_handler
router = APIRouter(prefix="/me", tags=["Me"])

@router.post("/check_in", response_model=BaseResponse, status_code=200)
async def create_streak(request: TrackerRequest):
    if request:
        pass
    err = db_handler.startStreak(check_date=request.date)
    print(err)
    return {
        "status": "success",
        "message": "Streak started"
    }


# TODO: implement function
@router.put("/check_in", response_model=BaseResponse, status_code=200)
async def end_streak(request: TrackerRequest):
    if request:
        pass
    err = db_handler.endStreak(close_date=request.date)
    return {
        "status": "success",
        "message": "Streak ended"
    }

@router.get("/streaks", response_model=TrackerResponse, status_code=200)
async def get_streaks():
    data, err = db_handler.getStreaks()
    answer = []
    if data:
        for streak in data:
            answer.append(TrackerData(id=streak.ID,
                                   user_id=streak.user_ID,
                                   start_date=streak.start_date,
                                   end_date=streak.end_date))
    return {
        "status": "success",
        "message": "Streaks retrieved",
        "data": answer
    }

# TODO: implement function
@router.get("/books", status_code=200)
async def get_user_books(request: Request, filt: Optional[str]):
    if request and filt:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "User books retrieved",
        "data": []  # Array of books
    })


# TODO: implement function, 404
@router.get("/books/{book_id}", status_code=200)
async def get_user_book(request: Request, book_id: int):
    if request and book_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "User book details retrieved",
        "data": {
            "book_id": uuid,
            "start_date": "2025-01-01",
            "end_date": "",
            "status": "reading"
        }
    })


# TODO: implement function, 404
@router.post("/books", status_code=200)
async def add_user_book(request: Request):
    if request:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "User book successfully added",
    })


# TODO: implement function, 404
@router.put("/books/{book_id}", status_code=200)
async def update_user_book(request: Request, book_id: int):
    if request and book_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "User book updated successfully"
    })


# TODO: implement function, 404
@router.delete("/books/{book_id}", status_code=200)
async def delete_user_book(request: Request, book_id: int):
    if request and book_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "User book deleted successfully"
    })


# TODO: Replace mockup
@router.get("/reviews/{review_id}", status_code=200)
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


# TODO: Replace mockup
@router.put("/reviews/{review_id}", status_code=200)
async def update_review(review_id: int):
    if review_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Review updated"
    })


# TODO: Replace mockup
@router.delete("/reviews/{review_id}", status_code=200)
async def delete_review(review_id: int):
    if review_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Review deleted"
    })


# TODO: Replace mockup
@router.post("/reviews", status_code=200)
async def create_review(review_id: int):
    if review_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Review created"
    })
