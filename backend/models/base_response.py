from pydantic import BaseModel
from typing import Literal


class BaseResponse(BaseModel):
    status: str = Literal["success", "error"]
    message: str
