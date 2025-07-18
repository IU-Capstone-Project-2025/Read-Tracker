import logging
import datetime

from fastapi import APIRouter, HTTPException
from uuid import UUID

from src.models.base_response import BaseResponse
from src.models.books import BookData
from src.models.tracker import TrackerRequest, TrackerResponse, TrackerData
from src.models.user import UserRequest
from src.models.user_books import UserBookResponse, UserBookData, UserBookRequest

from src.database.db_instance import db_handler

router = APIRouter(prefix="/me", tags=["Me"])
logging.basicConfig(level=logging.DEBUG)


@router.post("/check_in", response_model=BaseResponse, status_code=200)
async def update_streak(request: TrackerRequest):
    logging.info("Function update_streak from me.py is called")
    data, err = db_handler.getStreaks(user_id=request.user_id)
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data and not (data[-1].end_date or abs(datetime.datetime.now().date() - data[-1].last_marked).days <= 1):
        err = db_handler.endStreak(user_id=request.user_id)
        if err:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    err = db_handler.startStreak(user_id=request.user_id)
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.debug(data)
    for i in data:
        logging.debug(f"{i.id}, {i.user_id}, {i.start_date}, {i.end_date}, {i.last_marked}")
    logging.info("Function register_user succeeded")
    return {
        "status": "success",
        "message": "Checked in successfully"
    }


@router.post("/streaks", response_model=TrackerResponse, status_code=200)
async def get_streaks(request: TrackerRequest):
    data, err = db_handler.getStreaks(user_id=request.user_id)
    answer = []
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data:
        for streak in data:
            answer.append(TrackerData(
                id=streak.id,
                user_id=streak.user_id,
                start_date=streak.start_date,
                end_date=streak.end_date,
                last_marked=streak.last_marked
            ))
    return {
        "status": "success",
        "message": "Streaks retrieved",
        "data": answer
    }


@router.post("/books", response_model=UserBookResponse, status_code=200)
async def get_user_books(request: UserRequest):
    data, err = db_handler.getUserBooks(user_id=request.user_id)
    answer = []
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data:
        for user_book in data:
            answer.append(UserBookData(user_id=user_book.user_id,
                                       book_id=user_book.book_id,
                                       start_date=user_book.start_date,
                                       end_date=user_book.end_date,
                                       status=user_book.status))
    return {
        "status": "success",
        "message": "User books retrieved",
        "data": answer
    }


@router.post("/books/{book_id}", status_code=200)
async def get_user_book(request: UserRequest, book_id: UUID):
    data, err = db_handler.getUserBook(user_id=request.user_id, book_id=book_id)
    answer = []
    if err:
        if "No association found" in str(err):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": "User book not found"
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    if data:
        answer.append(UserBookData(user_id=data.user_id,
                                   book_id=data.book_id,
                                   start_date=data.start_date,
                                   end_date=data.end_date,
                                   status=data.status))
    return {
        "status": "success",
        "message": "Book details retrieved",
        "data": answer
    }


@router.post("/books/{book_id}/new", response_model=BaseResponse, status_code=200)
async def add_user_book(request: UserBookRequest, book_id: UUID):
    err = db_handler.addUserBook(user_id=request.user_id, book_id=book_id, status=request.status)
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    return {
        "status": "success",
        "message": "User book successfully added",
    }


@router.put("/books/{book_id}", response_model=BaseResponse, status_code=200)
async def update_user_book(request: UserBookRequest, book_id: UUID):
    err = db_handler.updateUserBook(user_id=request.user_id, book_id=book_id, status=request.status)
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    return {
        "status": "success",
        "message": "User book updated successfully"
    }


@router.delete("/books/{book_id}", response_model=BaseResponse, status_code=200)
async def delete_user_book(request: UserRequest, book_id: UUID):
    err = db_handler.deleteUserBook(user_id=request.user_id, book_id=book_id)
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    return {
        "status": "success",
        "message": "User book deleted successfully"
    }
