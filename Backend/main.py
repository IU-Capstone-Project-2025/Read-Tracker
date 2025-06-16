from fastapi import FastAPI
from Routes import auth, books, notes, reviews, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(notes.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.get('/', status_code=200)
async def start():
    return {"message": "Welcome to the webpage!"}