
from fastapi import APIRouter, HTTPException
from src.models.collections import (
    CollectionRequest,
    CollectionResponse,
    CollectionData,
    AddBookToCollectionRequest,
)
from src.models.base_response import BaseResponse
from src.database.db_instance import db_handler
from uuid import UUID

router = APIRouter(prefix="/me/collections", tags=["Collections"])


@router.get("", response_model=CollectionResponse, status_code=200)
async def get_collections():
    data, err = db_handler.getCollections()
    result = []

    if data:
        for collection in data:
            result.append(CollectionData(
                id=collection.id,
                title=collection.title,
                description=collection.description,
                cover=collection.cover,
                is_private=collection.is_private,
                created_at=collection.created_at,
                user_id=collection.user_id,
            ))

    return {
        "status": "success",
        "message": "Collections retrieved successfully",
        "data": result
    }


@router.get("/{collection_id}", response_model=CollectionResponse, status_code=200)
async def get_collection(collection_id: UUID):
    collection, err = db_handler.getCollection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    return {
        "status": "success",
        "message": "Collection fetched successfully",
        "data": [CollectionData(
            id=collection.id,
            title=collection.title,
            description=collection.description,
            cover=collection.cover,
            is_private=collection.is_private,
            created_at=collection.created_at,
            user_id=collection.user_id,
        )]
    }


@router.post("", response_model=BaseResponse, status_code=200)
async def create_collection(request: CollectionRequest):
    err = db_handler.addCollection(
        title=request.title,
        description=request.description,
        is_private=request.is_private,
        cover=request.cover,
    )
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to create collection")
    return {
        "status": "success",
        "message": "Collection created"
    }


@router.put("/{collection_id}", response_model=BaseResponse, status_code=200)
async def update_collection(request: CollectionRequest, collection_id: UUID):
    err = db_handler.updateCollection(
        collection_id=collection_id,
        title=request.title,
        description=request.description,
        is_private=request.is_private,
        cover=request.cover
    )
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to update the collection")
    return {
        "status": "success",
        "message": "Collection updated"
    }


@router.delete("/{collection_id}", response_model=BaseResponse, status_code=200)
async def delete_collection(collection_id: UUID):
    err = db_handler.deleteCollection(collection_id)
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to delete collection")
    return {
        "status": "success",
        "message": "Collection deleted"
    }


@router.post("/{collection_id}/books", response_model=BaseResponse, status_code=200)
async def add_book_to_collection(request: AddBookToCollectionRequest, collection_id: UUID):
    err = db_handler.addBookToCollection(
        collection_id=collection_id,
        book_id=request.book_id
    )
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to add book to collection")
    return {
        "status": "success",
        "message": "Book added to the collection"
    }


@router.delete("/{collection_id}/books/{book_id}", response_model=BaseResponse, status_code=200)
async def delete_book_from_collection(collection_id: UUID, book_id: UUID):
    err = db_handler.removeBookFromCollection(
        collection_id=collection_id,
        book_id=book_id
    )
    if err:
        print(err)
        raise HTTPException(status_code=500, detail="Failed to delete book from collection")
    return {
        "status": "success",
        "message": "Book deleted from the collection"
    }
