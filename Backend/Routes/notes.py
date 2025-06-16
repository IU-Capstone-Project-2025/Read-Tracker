from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/notes", tags=["Notes"])


# TODO: Replace mockup, 404 error
@router.get("/{note_id}", status_code=200)
async def get_review(note_id: int):
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
@router.put("/{note_id}", status_code=200)
async def update_review(request: Request, note_id: int):
    if request or note_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note updated",
    })


# TODO: Replace mockup; 404 error.
@router.delete("/{note_id}", status_code=200)
async def delete_book(note_id: int):
    if note_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Note deleted",
    })
