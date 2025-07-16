from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, books, collections, me, notes, subscriptions, reviews
from src.database import book_tag_setter

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(books.router)
app.include_router(notes.router)
app.include_router(collections.router)
app.include_router(me.router)
app.include_router(reviews.router)
app.include_router(subscriptions.router)

book_tag_setter.set_book_tags()


@app.get('/', status_code=200)
async def start():
    return {"message": "Welcome to the webpage!"}
