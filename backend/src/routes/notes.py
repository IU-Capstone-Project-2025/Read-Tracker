from fastapi import APIRouter, HTTPException
from src.models.notes import NoteResponse, NoteRequest, NoteData
from src.models.base_response import BaseResponse
from src.models.user import UserRequest
from src.database.db_instance import db_handler
from uuid import UUID

router = APIRouter(tags=["Notes"])


@router.get("/me/books/{book_id}/notes", response_model=NoteResponse, status_code=200)
async def get_notes(request: UserRequest, book_id: UUID):
    try:
        if not book_id:
            raise HTTPException(status_code=404, detail="Book id not found")
        data, err = db_handler.getNotes(user_id=request.user_id, book_id=book_id)
        answer = []
        if data:
            for note in data:
                answer.append(NoteData(
                    id=note.id,
                    text=note.text,
                    book_id=note.book_id,
                    user_id=note.user_id,
                    created_at=note.created_at
                ))
        return {
            "status": "success",
            "message": "Note details retrieved",
            "data": answer
        }
    except Exception as e:
        print(data)
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/me/books/{book_id}/notes", response_model=BaseResponse, status_code=200)
async def add_note(request: NoteRequest, book_id: UUID):
    if not book_id:
        raise HTTPException(status_code=404, detail="Book id not found")
    err = db_handler.addNote(book_id=book_id, user_id=request.user_id, text=request.text)
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to add note")
    return {
        "status": "success",
        "message": "Note added",
    }


@router.get("/me/notes/{note_id}", response_model=NoteResponse, status_code=200)
async def get_note(note_id: UUID):
    if not note_id:
        raise HTTPException(status_code=404, detail="Note id not found")
    data, err = db_handler.getNote(note_id=note_id)
    answer = []
    if data:
        answer = [NoteData(
            id=data.id,
            text=data.text,
            book_id=data.book_id,
            user_id=data.user_id,
            created_at=data.created_at
        )]
    return {
        "status": "success",
        "message": "Note details retrieved",
        "data": answer
    }


@router.put("/me/notes/{note_id}", response_model=BaseResponse, status_code=200)
async def update_note(request: NoteRequest, note_id: UUID):
    if not note_id:
        raise HTTPException(status_code=404, detail="Note id not found")
    if not request or not request.text:
        raise HTTPException(status_code=400, detail="Invalid note")
    err = db_handler.updateNote(note_id=note_id, text=request.text)
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to update note")
    return {
        "status": "success",
        "message": "Note updated",
    }


@router.delete("/me/notes/{note_id}", response_model=BaseResponse, status_code=200)
async def delete_note(note_id: UUID):
    if not note_id:
        raise HTTPException(status_code=404, detail="Note id not found")
    err = db_handler.deleteNote(note_id=note_id)
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to delete note")
    return {
        "status": "success",
        "message": "Note deleted",
    }
