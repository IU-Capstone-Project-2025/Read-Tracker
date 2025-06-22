from fastapi import FastAPI, Response, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


# TODO: Check 400 and 409 error cases; Code validation process.
@router.post("/register")
async def register_user(request: Request):
    """
    {
    "email": "user@example.com",
    "password": "password"
    }
    """
    data = await request.json()
    if not data:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "User registered successfully."
    }, status_code=201)


# TODO: 401 and 404 errors. Code validation
@router.post("/login")
async def login_user(request: Request):
    """
    {
    "mail": "user@example.com",
    "password": "secure_password123"
    }
    """
    data = await request.json()
    if not data:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "User logged in successfully.",
        "token": "abc123...",  # JWT or session token
        "user_id": 123    # uuid
    }, status_code=200)


# TODO: 404 error
@router.post("/validate", status_code=200)
async def validate_token(request: Request):
    if request:
        pass
    return JSONResponse(content={
        "status": "success",
        "message": "Token validated",
    }, status_code=200)


# TODO: 404 error
@router.post("/refresh", status_code=200)
async def refresh_token(request: Request):
    if request:
        pass
    return JSONResponse(content={
        "status": "success",
        "token": "abc123...",  # JWT or session token
    }, status_code=200)


# TODO: Code validation process; 400 and 404 errors
@router.post("forgot_password")
async def forgot_password(request: Request):
    data = await request.json()
    if not data:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "If the email is registered, a reset link has been sent."
    }, status_code=200)


# TODO: Code validation; 400 error.
@router.post("reset_password")
async def reset_password(request: Request):
    data = await request.json()
    if not data:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Password updated successfully"
    }, status_code=200)


# TODO: 401 error
@router.get("/profile", status_code=200)
async def get_user_profile(request: Request):
    if request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "User fetched successfully",
        "data": {
            "id": "uuid",
            "username": "Username",
            "email": "user@example.com"
        }
    })


# TODO: 400, 401 error
@router.put("/profile/avatar", status_code=200)
async def update_avatar(request: Request):
    if request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Avatar updated",
    })


# TODO: 400, 401 error
@router.put("/profile/password", status_code=200)
async def change_password(request: Request):
    if request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Password changed successfully",
    })
