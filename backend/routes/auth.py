from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from models.base_response import BaseResponse
from models.auth import LoginRequest, EmailRequest, PasswordRestoreRequest, RegisterRequest, LoginResponse
from modeules.user import UserRequest, UserData, UserResponse
from database.db_instance import db_handler
import logging

router = APIRouter(prefix="/auth", tags=["Auth"])


# TODO: Check 400 and 409 error cases; Code validation process.
@router.post("/register", response_model=BaseResponse, status_code=201)
async def register_user(request: RegisterRequest):
    logging.info("Function register_user from auth.py is called")
    err = db_handler.registerUser(name=request.name,
                                  email=request.email,
                                  password=request.password)
    if err:
        logging.error(f"Database returned error: {err}")
        return {
            "status": "error",
            "message": err
        }
    logging.info("Function register_user succeeded")
    return {
        "status": "success",
        "message": "User registered successfully."
    }


# TODO: 401 and 404 errors. Code validation
@router.post("/login", response_model=LoginResponse, status_code=200)
async def login_user(request: LoginRequest):
    logging.info("Function login_user from auth.py is called")
    """
    {
    "mail": "user@example.com",
    "password": "secure_password123"
    }
    """
    data, err = db_handler.loginUser(mail=request.email,
                                     password=request.password)
    logging.debug(f"Data: {data}")
    if err:
        raise HTTPException(status_code=404, detail=err)

    return {
        "status": "success",
        "message": "User logged in successfully.",
        "user_id": data   # uuid
    }


# TODO: Code validation process; 400 and 404 errors
@router.post("forgot_password", response_model=BaseResponse)
async def forgot_password(request: PasswordRestoreRequest):
    data = await request.json()
    if not data:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "If the email is registered, a reset link has been sent."
    }, status_code=200)


# TODO: Code validation; 400 error.
@router.post("reset_password", response_model=BaseResponse)
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
    data, err = getUser(request.user_id)
    return {
        "status": "success",
        "message": "User fetched successfully",
        "data": {
            "id": data.id,
            "username": data.name,
            "email": data.mail,
            "avatar": data.avatar
        }
    }


# TODO: 400, 401 error
@router.put("/profile/avatar", response_model=BaseResponse, status_code=200)
async def update_avatar(request: Request):
    if request:
        pass
    err = db_handler.updateAvatar(user_id=request.user_id,
                                  avatar=request.avatar)
    return {
        "status": "success",
        "message": "Avatar updated",
    }


# TODO: 400, 401 error
@router.put("/profile/password", response_model=BaseResponse, status_code=200)
async def change_password(request: Request):
    if request:
        pass

    return JSONResponse(content={
        "status": "success",
        "message": "Password changed successfully",
    })


"""
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
"""