from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.envelope import ok
from app.core.logging import configure_logging
from app.db.client import connect, disconnect
from app.middleware.error_handler import add_exception_handlers
from app.modules.auth.router import router as auth_router
from app.modules.lead.router import router as lead_router
from app.modules.contact.router import router as contact_router
from app.modules.account.router import router as account_router
from app.modules.pipeline.router import router as pipeline_router
from app.modules.activity.router import router as activity_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await connect()
    yield
    await disconnect()


app = FastAPI(title="CRM API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app)

app.include_router(auth_router)
app.include_router(lead_router, prefix="/api/v1")
app.include_router(contact_router, prefix="/api/v1")
app.include_router(account_router, prefix="/api/v1")
app.include_router(pipeline_router, prefix="/api/v1")
app.include_router(activity_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict:
    return ok({"status": "ok"})
