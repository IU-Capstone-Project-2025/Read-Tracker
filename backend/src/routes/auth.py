from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from src.models.base_response import BaseResponse
from src.models.auth import LoginRequest, PasswordRestoreRequest, RegisterRequest, LoginResponse
from src.models.user import UserRequest, UpdateAvatarRequest
from src.database.db_instance import db_handler
import logging
import re
router = APIRouter(prefix="/auth", tags=["Auth"])

logging.basicConfig(level=logging.DEBUG)


@router.post("/register", response_model=BaseResponse, status_code=201)
async def register_user(request: RegisterRequest):
    logging.info("Function register_user from auth.py is called")
    email_template = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if not re.fullmatch(email_template, request.email, re.IGNORECASE):
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mail is invalid"
        })
    err = db_handler.registerUser(name=request.name,
                                  email=request.email,
                                  password=request.password)
    if err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function register_user succeeded")
    return {
        "status": "success",
        "message": "User registered successfully."
    }


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login_user(request: LoginRequest):
    logging.info("Function login_user from auth.py is called")
    logging.debug(f"Login payload: {request}")

    data, err = db_handler.loginUser(mail=request.email,
                                     password=request.password)
    logging.debug(f"Data: {data}")
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=401, detail={
                "status": "error",
                "message": "No user found or password mismatch. Not authorized"
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })

    return {
        "status": "success",
        "message": "User logged in successfully.",
        "user_id": data   # uuid
    }


@router.post("/profile", status_code=200)
async def get_user_profile(request: UserRequest):
    logging.info("Function get_user_profile from auth.py is called")
    data, err = db_handler.getUser(request.user_id)
    if not data:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": "No user found"
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    logging.info("Function get_user_profile succeeded")
    logging.debug(data.created_at)
    return {
        "status": "success",
        "message": "User fetched successfully",
        "data": {
            "id": data.id,
            "username": data.name,
            "email": data.mail,
            "avatar": data.avatar,
            "created_at": data.created_at
        }
    }


@router.put("/profile/avatar", response_model=BaseResponse, status_code=200)
async def update_avatar(request: UpdateAvatarRequest):
    logging.info("Function update_avatar from auth.py is called")
    err = db_handler.updateAvatar(user_id=request.user_id,
                                  avatar=request.avatar)
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": "No user found."
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    logging.info("Function update_avatar succeeded")
    return {
        "status": "success",
        "message": "Avatar updated",
    }


@router.put("/profile/password", response_model=BaseResponse, status_code=200)
async def change_password(request: PasswordRestoreRequest):
    logging.info("Function change_password from auth.py is called")
    err = db_handler.resetPassword(password=request.password, user_id=request.user_id)
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": "No user found."
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    logging.info("Function change_password succeeded")
    return {
        "status": "success",
        "message": "Password changed successfully",
    }
