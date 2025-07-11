from pydantic import BaseModel
from uuid import UUID
from src.models.base_response import BaseResponse


class LoginRequest(BaseModel):
    email: str
    password: str


class EmailRequest(BaseModel):
    email: str


class PasswordRestoreRequest(BaseModel):
    user_id: UUID
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class LoginResponse(BaseResponse):
    user_id: UUID
