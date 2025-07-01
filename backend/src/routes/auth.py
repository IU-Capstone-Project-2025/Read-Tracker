from fastapi import FastAPI, Response, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from src.models.base_response import BaseResponse
from src.models.auth import LoginRequest, EmailRequest, PasswordRestoreRequest, RegisterRequest, LoginResponse
from src.models.user import UserRequest, UserData, UserResponse, UpdateAvatarRequest
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


@router.get("/profile", status_code=200)
async def get_user_profile(request: UserRequest):
    logging.info("Function get_user_profile from auth.py is called")
    data, err = db_handler.getUser(request.user_id)
    if not data:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": "No user found"
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    logging.info("Function get_user_profile succeeded")
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
async def update_avatar(request: UpdateAvatarRequest):
    logging.info("Function update_avatar from auth.py is called")
    err = db_handler.updateAvatar(user_id=request.user_id,
                                  avatar=request.avatar)
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=400, detail={
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


# TODO: 400, 401 error
@router.put("/profile/password", response_model=BaseResponse, status_code=200)
async def change_password(request: PasswordRestoreRequest):
    logging.info("Function change_password from auth.py is called")
    if request:
        pass
    err = db_handler.resetPassword(password=request.password, user_id=request.user_id)
    if err:
        if isinstance(err, ValueError):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": "No user found."
            })
        else:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": str(err)
            })
    logging.info("Function change_password succeeded")
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

"""
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
"""