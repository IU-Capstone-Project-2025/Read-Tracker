from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from src.models.base_response import BaseResponse
from src.models.user import UserRequest

class LoginRequest(BaseModel):
    email: str
    password: str


class EmailRequest(BaseModel):
    email: str


class PasswordRestoreRequest(UserRequest):
    password: str


class RegisterRequest(LoginRequest):
    name: str


class LoginResponse(BaseResponse):
    user_id: UUID
