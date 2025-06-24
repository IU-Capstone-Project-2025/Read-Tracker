from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional

router = APIRouter(prefix="/feed", tags=["Feed"])


# TODO: implement code
@router.get("/collections", status_code=200)
async def get_collections(limit: int, offset: int, user_id: Optional[int]):
    if limit and offset and user_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "collections retrieved successfully",
        "data": {
            "items": [],
            "pagination": {
                "limit": 10,
                "offset": 20,
                "total": 123
            }
        }
    })


# TODO: implement code
@router.get("/reviews", status_code=200)
async def get_reviews(limit: int, offset: int, user_id: Optional[int]):
    if limit and offset and user_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "collections retrieved successfully",
        "data": {
            "items": [],
            "pagination": {
                "limit": 10,
                "offset": 20,
                "total": 123
            }
        }
    })
