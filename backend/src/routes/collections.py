from fastapi import APIRouter, HTTPException
from src.models.collections import (
    CollectionRequest,
    CollectionResponse,
    CollectionData,
    CollectionRequestWithUserID
)
from src.models.user import UserRequest
from src.models.base_response import BaseResponse
from src.database.db_instance import db_handler
from src.models.books import BookData
from uuid import UUID
import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter(prefix="/me/collections", tags=["Collections"])


@router.get("/{collection_id}", response_model=CollectionResponse, status_code=200)
async def get_collection(collection_id: UUID):
    collection, collection_err = db_handler.getCollection(collection_id)
    collection_books, collection_book_err = db_handler.getCollectionItems(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    if collection_err or collection_book_err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": f"GetCollection error (might be empty): {str(collection_err)},"
                       f"GetCollectionItems error (might be empty): {str(collection_book_err)} "
        })

    books = []
    if collection_books:
        for book in collection_books:
            tag_objects, tag_err = db_handler.getTags(book.id)
            if tag_err:
                if isinstance(err, ValueError):
                    raise HTTPException(status_code=404, detail={
                        "status": "error",
                        "message": "Book not found."
                    })
                else:
                    raise HTTPException(status_code=400, detail={
                        "status": "error",
                        "message": str(err)
                    })
            tags = []
            for tag in tag_objects:
                tags.append(TagData(id=tag.id,
                                    name=tag.name,
                                    description=tag.description))
            books.append(BookData(id=book.id,
                                  author=book.author,
                                  title=book.title,
                                  language=book.language,
                                  description=book.description,
                                  cover=book.cover,
                                  tags=tags))
    logging.debug(books)
    logging.info("Function completed successfully")
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
            items=books
        )]
    }


@router.post("/all", response_model=CollectionResponse, status_code=200)
async def get_collections(request: UserRequest):
    logging.info(f"Function get_collections is called")
    data, err = db_handler.getCollections(request.user_id)
    result = []
    if err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data:
        for collection in data:
            result.append(CollectionData(
                id=collection.id,
                user_id=collection.user_id,
                title=collection.title,
                description=collection.description,
                cover=collection.cover,
                is_private=collection.is_private,
                created_at=collection.created_at,
            ))
    logging.info("Function completed successfully")
    return {
        "status": "success",
        "message": "Collections retrieved successfully",
        "data": result
    }
    

@router.post("", response_model=BaseResponse, status_code=200)
async def create_collection(request: CollectionRequestWithUserID):
    err = db_handler.addCollection(
        user_id=request.user_id,
        title=request.title,
        description=request.description,
        is_private=request.is_private,
        cover=request.cover,
    )
    if err:

        print(err)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function completed successfully")
    return {
        "status": "success",
        "message": "Collection created"
    }


@router.put("/{collection_id}", response_model=BaseResponse, status_code=200)
async def update_collection(request: CollectionRequest, collection_id: UUID):
    logging.info("Function update_collection is called")
    err = db_handler.updateCollection(
        collection_id=collection_id,
        title=request.title,
        description=request.description,
        is_private=request.is_private,
        cover=request.cover
    )
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": "Collecction not found."
            })
        print(err)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function completed successfully")
    return {
        "status": "success",
        "message": "Collection updated"
    }


@router.delete("/{collection_id}", response_model=BaseResponse, status_code=200)
async def delete_collection(collection_id: UUID):
    err = db_handler.deleteCollection(collection_id)
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": "Collection not found."
            })
        print(err)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function completed successfully")
    return {
        "status": "success",
        "message": "Collection deleted"
    }


@router.post("/{collection_id}/{book_id}", response_model=BaseResponse, status_code=200)
async def add_book_to_collection(collection_id: UUID, book_id: UUID):
    err = db_handler.addBookToCollection(
        collection_id=collection_id,
        book_id=book_id
    )
    if err:
        print(err)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function completed successfully")
    return {
        "status": "success",
        "message": "Book added to the collection"
    }


@router.delete("/{collection_id}/{book_id}", response_model=BaseResponse, status_code=200)
async def delete_book_from_collection(collection_id: UUID, book_id: UUID):
    err = db_handler.deleteBookFromCollection(
        collection_id=collection_id,
        book_id=book_id
    )
    if err:
        print(err)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function completed successfully")
    return {
        "status": "success",
        "message": "Book deleted from the collection"
    }
