import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.middleware.error_handler import add_exception_handlers, NotFoundError, ForbiddenError


def make_app() -> FastAPI:
    test_app = FastAPI()
    add_exception_handlers(test_app)

    class Body(BaseModel):
        name: str
        age: int

    @test_app.post("/validate")
    async def validate_body(body: Body):
        return {"ok": True}

    @test_app.get("/not-found")
    async def not_found():
        raise NotFoundError("Thing not found")

    @test_app.get("/forbidden")
    async def forbidden():
        raise ForbiddenError()

    return test_app


def test_validation_error_returns_422_fields() -> None:
    client = TestClient(make_app(), raise_server_exceptions=False)
    res = client.post("/validate", json={"name": "ok"})
    assert res.status_code == 422
    body = res.json()
    assert body["error"]["message"] == "Validation error"
    assert any("age" in d["field"] for d in body["error"]["details"])


def test_not_found_returns_404() -> None:
    client = TestClient(make_app(), raise_server_exceptions=False)
    res = client.get("/not-found")
    assert res.status_code == 404
    assert res.json()["error"]["message"] == "Thing not found"


def test_forbidden_returns_403() -> None:
    client = TestClient(make_app(), raise_server_exceptions=False)
    res = client.get("/forbidden")
    assert res.status_code == 403
