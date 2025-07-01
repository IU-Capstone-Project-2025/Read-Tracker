from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import sys
from typing import Optional
from uuid import UUID

sys.path.append('../..')
from src.models.base_response import BaseResponse
from src.models.tracker import TrackerRequest, TrackerResponse, TrackerData
from src.database.db_instance import db_handler

router = APIRouter(prefix="/me", tags=["Me"])


@router.post("/check_in", response_model=BaseResponse, status_code=200)
async def create_streak(request: TrackerRequest):
    if not request:
        raise HTTPException(status_code=400, detail="Invalid request")
    err = db_handler.startStreak(check_date=request.date)
    print(err)
    return {
        "status": "success",
        "message": "Streak started"
    }


@router.put("/check_in", response_model=BaseResponse, status_code=200)
async def end_streak(request: TrackerRequest):
    if not request:
        raise HTTPException(status_code=400, detail="Invalid request")
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
            answer.append(TrackerData(
                id=streak.id,
                user_id=streak.user_id,
                start_date=streak.start_date,
                end_date=streak.end_date
            ))
    return {
        "status": "success",
        "message": "Streaks retrieved",
        "data": answer
    }


@router.get("/books", status_code=200)
async def get_user_books(request: Request, filt: Optional[str] = None):
    # TODO: Implement function logic based on filt and user from request
    return JSONResponse(content={
        "status": "success",
        "message": "User books retrieved",
        "data": []  # Array of user books
    })


@router.get("/books/{book_id}", status_code=200)
async def get_user_book(request: Request, book_id: UUID):
    # TODO: Implement fetching user book by book_id
    return JSONResponse(content={
        "status": "success",
        "message": "User book details retrieved",
        "data": {
            "book_id": str(book_id),
            "start_date": "2025-01-01",
            "end_date": None,
            "status": "reading"
        }
    })


@router.post("/books", status_code=200)
async def add_user_book(request: Request):
    # TODO: Implement adding user book
    return JSONResponse(content={
        "status": "success",
        "message": "User book successfully added",
    })


@router.put("/books/{book_id}", status_code=200)
async def update_user_book(request: Request, book_id: UUID):
    # TODO: Implement updating user book
    return JSONResponse(content={
        "status": "success",
        "message": "User book updated successfully"
    })


@router.delete("/books/{book_id}", status_code=200)
async def delete_user_book(request: Request, book_id: UUID):
    # TODO: Implement deleting user book
    return JSONResponse(content={
        "status": "success",
        "message": "User book deleted successfully"
    })
