from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from models.base_response import BaseResponse
from models.tracker import TrackerRequest
from typing import Optional
from database.db_instance import db_handler
router = APIRouter(prefix="/me", tags=["Me"])


# TODO: implement function
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

# "2025-06-25T18:05:53.563505"

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