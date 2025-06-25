from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from ..models.notes import NoteResponse, NoteRequest
from ..models.base_response import BaseResponse
router = APIRouter(tags=["Notes"])


# TODO: Replace mockup, 404 error
@router.get("/me/books/{book_id}/notes", status_code=200)
async def get_notes(book_id: int):
    if book_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note details retrieved",
        "data": []
    })


# TODO: Replace mockup, 404 error
@router.post("/me/books/{book_id}/notes", status_code=200)
async def add_note(note_id: int):
    if note_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note details retrieved",
        "data": {
            "id": 123,
            "content_type": type,
            "text": "Note text here",
            "book_id": 123,
            "created_at": 123,
          }
    })


# TODO: Replace mockup, 404 error
@router.get("/me/notes/{note_id}", status_code=200)
async def get_note(note_id: int):
    if note_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note details retrieved",
        "data": {
            "id": 123,
            "content_type": type,
            "text": "Note text here",
            "book_id": 123,
            "created_at": 123,
          }
    })


# TODO: Replace mockup; Code validation steps, 400, 404 errors.
@router.put("/me/notes/{note_id}", status_code=200)
async def update_note(request: Request, note_id: int):
    if request or note_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note updated",
    })


# TODO: Replace mockup; 404 error.
@router.delete("/me/notes/{note_id}", status_code=200)
async def delete_note(note_id: int):
    if note_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note deleted",
    })
