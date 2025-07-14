from fastapi import APIRouter

from src.database.db_instance import db_handler
from src.models.books import BookData, BookResponse, TagData

import logging

logging.basicConfig(level=logging.DEBUG)
router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=BookResponse, status_code=200)
async def get_books():
    data, err = db_handler.getBooks()
    answer = []
    if err:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data:
        for book in data:
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
            answer.append(BookData(id=book.id,
                                   author=book.author,
                                   title=book.title,
                                   language=book.language,
                                   description=book.description,
                                   cover=book.cover,
                                   tags=tags))
    logging.debug(answer)
    return {
        "status": "success",
        "message": "Books retrieved",
        "data": answer
    }


@router.get("/{book_id}", response_model=BookResponse, status_code=200)
async def get_book(book_id: int):
    if book_id:
        pass
    data, err = db_handler.getBook(book_id=book_id)
    answer = []
    if err:
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
    if data:
        for book in data:
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
            answer.append(BookData(id=book.id,
                                   author=book.author,
                                   title=book.title,
                                   language=book.language,
                                   description=book.description,
                                   cover=book.cover,
                                   tags=tags))
    logging.debug(answer)
    return {
        "status": "success",
        "message": "Book details retrieved",
        "data": answer
    }
