from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from ..models.notes import NoteResponse, NoteRequest
from ..models.base_response import BaseResponse
router = APIRouter(tags=["Notes"])


# TODO: Replace mockup, 404 error
@router.get("/me/books/{book_id}/notes", response_model=NoteResponse, status_code=200)
async def get_notes(book_id: int):
    if not book_id:
        raise HTTPException(status_code=404,
                            detail="Book id not found")
    data = []
    return {
        "status": "success",
        "message": "Note details retrieved",
        "data": data
    }


# TODO: Replace mockup, 404 error
@router.post("/me/books/{book_id}/notes", response_model=BaseResponse, status_code=200)
async def add_note(request: NoteRequest, book_id: int):
    if not book_id:
        raise HTTPException(status_code=404,
                            detail="Book id not found")
    return {
        "status": "success",
        "message": "Note details retrieved",
    }


# TODO: Replace mockup, 404 error
@router.get("/me/notes/{note_id}", response_model=NoteResponse, status_code=200)
async def get_note(note_id: int):
    if not note_id:
        raise HTTPException(status_code=404,
                            detail="Note id not found")

    return {
        "status": "success",
        "message": "Note details retrieved",
        "data": {
            "id": 123,
            "text": "Note text here",
            "book_id": 123,
            "created_at": 123,
        }
    }


# TODO: Replace mockup; Code validation steps, 400, 404 errors.
@router.put("/me/notes/{note_id}", response_model=BaseResponse, status_code=200)
async def update_note(request: NoteRequest, note_id: int):
    if not note_id:
        raise HTTPException(status_code=404,
                            detail="Note id not found")
    if not request:
        raise HTTPException(status_code=400,
                            detail="Invalid note")
    return {
        "status": "success",
        "message": "Note updated",
    }


# TODO: Replace mockup; 404 error.
@router.delete("/me/notes/{note_id}", response_model=BaseResponse, status_code=200)
async def delete_note(note_id: int):
    if not note_id:
        raise HTTPException(status_code=404,
                            detail="Note id not found")
    return {
        "status": "success",
        "message": "Note deleted",
    }
