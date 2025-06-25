from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from models.notes import NoteResponse, NoteRequest, NoteData
from models.base_response import BaseResponse
from database.db_instance import db_handler
from uuid import UUID
router = APIRouter(tags=["Notes"])


# TODO: Replace mockup, 404 error
@router.get("/me/books/{book_id}/notes", response_model=NoteResponse, status_code=200)
async def get_notes(book_id: UUID):
    try:
        if not book_id:
            raise HTTPException(status_code=404,
                                detail="Book id not found")
        data, err = db_handler.getNotes(book_id=book_id)
        answer = []
        if data:
            for note in data:
                answer.append(NoteData(id=note.ID,
                                       text=note.text,
                                       book_id=note.book_ID,
                                       user_id=note.user_ID,
                                       created_at=note.created_at))
        return {
            "status": "success",
            "message": "Note details retrieved",
            "data": answer
        }
    except Exception as e:
        print(data)
        print(e)


# TODO: Replace mockup, 404 error
@router.post("/me/books/{book_id}/notes", response_model=BaseResponse, status_code=200)
async def add_note(request: NoteRequest, book_id: UUID):
    if not book_id:
        raise HTTPException(status_code=404,
                            detail="Book id not found")
    err = db_handler.addNote(book_id=book_id, text=request.text)
    if err:
        print(err)
    return {
        "status": "success",
        "message": "Note added",
    }


# TODO: Replace mockup, 404 error
@router.get("/me/notes/{note_id}", response_model=NoteResponse, status_code=200)
async def get_note(note_id: UUID):
    if not note_id:
        raise HTTPException(status_code=404,
                            detail="Note id not found")
    data, err = db_handler.getNote(note_id=note_id)
    answer = []
    if data:
        answer = [NoteData(id=data.ID,
                          text=data.text,
                          book_id=data.book_ID,
                          user_id=data.user_ID,
                          created_at=data.created_at)]
    return {
        "status": "success",
        "message": "Note details retrieved",
        "data": answer
    }


# TODO: Replace mockup; Code validation steps, 400, 404 errors.
@router.put("/me/notes/{note_id}", response_model=BaseResponse, status_code=200)
async def update_note(request: NoteRequest, note_id: UUID):
    if not note_id:
        raise HTTPException(status_code=404,
                            detail="Note id not found")
    if not request:
        raise HTTPException(status_code=400,
                            detail="Invalid note")
    err = db_handler.updateNote(note_id=note_id, text=request.text)
    return {
        "status": "success",
        "message": "Note updated",
    }


# TODO: Replace mockup; 404 error.
@router.delete("/me/notes/{note_id}", response_model=BaseResponse, status_code=200)
async def delete_note(note_id: UUID):
    if not note_id:
        raise HTTPException(status_code=404,
                            detail="Note id not found")
    err = db_handler.deleteNote(note_id=note_id)
    return {
        "status": "success",
        "message": "Note deleted",
    }
