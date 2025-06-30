from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from models.base_response import BaseResponse


class LoginRequest(BaseModel):
    email: str
    password: str


class EmailRequest(BaseModel):
    email: str


class PasswordRestoreRequest(BaseModel):
    password: str


class RegisterRequest(LoginRequest):
    name: str


class LoginResponse(BaseResponse):
    user_id: uuid
