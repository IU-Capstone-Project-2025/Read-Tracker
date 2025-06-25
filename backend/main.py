from fastapi import FastAPI
from routes import auth, books, collections, feed, me, notes, subscriptions, reviews


app = FastAPI()


app.include_router(auth.router)
app.include_router(books.router)
app.include_router(notes.router)
app.include_router(collections.router)
app.include_router(feed.router)
app.include_router(me.router)
app.include_router(reviews.router)
app.include_router(subscriptions.router)


@app.get('/', status_code=200)
async def start():
    return {"message": "Welcome to the webpage!"}
