from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/books", tags=["Books"])


# TODO: Replace mockup
@router.get("/", status_code=200)
async def get_books():
    return JSONResponse(content={
        "status": "success",
        "message": "Books retrieved",
        "data": []  # Array of books (may be empty if no books)
    })


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
