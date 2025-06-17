from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/me/collections", tags=["Collections"])


# TODO: implement
@router.get("/", status_code=200)
async def get_collections():
    return JSONResponse(content={
        "status": "success",
        "message": "collections retrieved successfully",
        "data": []
    })


# TODO: implement
@router.get("/{collection_id}", status_code=200)
async def get_collection(collection_id: int):
    if collection_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Collection fetched successfully",
        "data":
            {
                "collection_id": 123,
                "title": "Collection",
                "description": "descriptions",
                "cover": "https://...",
                "user_id": 123,
                "username": "username",
                "is_private": False,
                "created_at": 123,
            }
    })


# TODO: implement
@router.post("/", status_code=200)
async def create_collection(request: Request):
    if request:
        pass
    return JSONResponse(content={
      "status": "success",
      "message": "Collection created"
    })


# TODO: implement
@router.put("/{collection_id}", status_code=200)
async def update_collection(request: Request, collection_id: int):
    if collection_id and request:
        pass
    return JSONResponse(content={
        "title": "new title",
        "description": "new description",
        "is_private": false,
        "cover": "https://..."
    })


# TODO: implement
@router.delete("/{collection_id}", status_code=200)
async def delete_collection(collection_id: int):
    if collection_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Collection deleted"
    })


# TODO: implement
@router.post("/{collection_id}/books", status_code=200)
async def add_book_to_collection(request: Request, collection_id: int):
    if request and collection_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Book added to the collection"
    })


# TODO: implement
@router.delete("/{collection_id}/books/{book_id}", status_code=200)
async def delete_book_from_collection(request: Request, collection_id: int, book_id: int):
    if request and collection_id and book_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Book deleted from the collection"
    })
