from typing import Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    data: Any = None
    error: Any = None
    meta: dict[str, Any] = {}


def ok(data: Any, meta: dict[str, Any] | None = None) -> dict:
    return ApiResponse(data=data, meta=meta or {}).model_dump()


def err(message: str, details: Any = None) -> dict:
    return ApiResponse(error={"message": message, "details": details}).model_dump()
