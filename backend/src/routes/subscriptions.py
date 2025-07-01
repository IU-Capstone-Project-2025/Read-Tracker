from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


# TODO: implement code, 404
@router.post("/", status_code=200)
async def subscribe(request: Request):
    if request:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Subscribed successfully"
    })


# TODO: implement code, 404
@router.delete("/{subscribed_id}", status_code=200)
async def unsubscribe(request: Request, subscribed_id: int):
    if request and subscribed_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Unsubscribed successfully"
    })


# TODO: Replace mockup
@router.get("/{subscribed_id}/reviews", status_code=200)
async def get_reviews(subscribed_id: int):
    if subscribed_id:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Reviews retrieved",
        "data": []
    })
