from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    traceback: str | None = None
    detail: dict | None = None
