from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from database.db_instance import db_handler
from models.base_response import BaseResponse
from models.books import BookData, BookResponse
router = APIRouter(prefix="/books", tags=["Books"])


# TODO: Replace mockup
@router.get("/", response_model=BookResponse, status_code=200)
async def get_books():
    data, err = db_handler.getBooks()
    answer = []
    if data:
        for book in data:
            answer.append(BookData(id=book.ID,
                                   author=book.author,
                                   title=book.title,
                                   language=book.language,
                                   description=book.description,
                                   cover=book.cover))
    return {
        "status": "success",
        "message": "Books retrieved",
        "data": answer
    }


# TODO: Replace mockup, 404 error
@router.get("/{book_id}", status_code=200)
async def get_book(book_id: int):
    if book_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Book details retrieved",
        "data": {
            "id": "uuid",
            "title": "Book Title",
            "author": "Author Name",
            "language": "lang",
            "cover": "https://cdn.example.com/cover.jpg",
            "status": "not started"  # or "reading" or "finished"
        }
    })


# TODO: Replace mockup; Code validation steps, 400, 404 errors
@router.post("/", status_code=200)
async def add_book(request: Request):
    if request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Book added",
        "data": {
            "id": "uuid",
            "title": "Book Title",
            "author": "Author Name",
            "language": "lang",
            "cover": "https://cdn.example.com/cover.jpg",
            "status": "not started"  # or "reading" or "finished"
        }
    })


# TODO: Replace mockup; Code validation steps, 400, 404 errors.
@router.put("/{book_id}", status_code=200)
async def update_book(request: Request, book_id: int):
    if request or book_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Book updated",

    })


# TODO: Replace mockup; 404 error.
@router.delete("/{book_id}", status_code=200)
async def delete_book(book_id: int):
    if book_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Book deleted",

    })


# TODO: Replace mockup
@router.get("/{book_id}/reviews", status_code=200)
async def get_reviews(book_id: int):
    if book_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Reviews retrieved",
        "data": []
    })


# TODO: Replace mockup
@router.get("/{book_id}/notes", status_code=200)
async def get_book_notes(request: Request, book_id: int):
    if book_id and request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Notes retrieved",
        "data": []
    })


# TODO: Replace mockup
@router.post("/{book_id}/notes", status_code=200)
async def add_book_note(request: Request, book_id: int):
    if book_id and request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note added",
        "data": []
    })
