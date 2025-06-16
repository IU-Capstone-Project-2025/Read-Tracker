from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users", tags=["Users"])


# TODO: Replace mockup
@router.get("/{user_id}", status_code=200)
async def get_profile(user_id: int):
    if user_id:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Profile retrieved",
        "data": {
            "id": "uuid",
            "username": "Username",
            "avatar": "https://cdn.example.com/avatar.jpg",
            "isVisible": true
        }
    })


# TODO: Replace mockup; 400 error
@router.put("/{user_id}/avatar", status_code=200)
async def update_avatar(request: Request, user_id: int):
    if user_id and request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Avatar updated"
    })


# TODO: Replace mockup
@router.put("/{user_id}/visibility", status_code=200)
async def set_visibility(request: Request, user_id: int):
    if user_id and request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Visibility changed"
    })


# TODO: Replace mockup, Code validation steps; 400 error
@router.put("/{user_id}/password", status_code=200)
async def change_password(request: Request, user_id: int):
    if user_id and request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Password changed successfully"
    })
