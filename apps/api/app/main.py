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
from app.modules.ticket.router import router as ticket_router
from app.modules.sla.router import router as sla_router
from app.modules.kb.router import router as kb_router
from app.modules.integration.router import router as integration_router
from app.modules.project.router import router as project_router
from app.modules.contract.router import router as contract_router
from app.modules.invoice.router import router as invoice_router


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
app.include_router(ticket_router, prefix="/api/v1")
app.include_router(sla_router, prefix="/api/v1")
app.include_router(kb_router, prefix="/api/v1")
app.include_router(integration_router, prefix="/api/v1")
app.include_router(project_router, prefix="/api/v1")
app.include_router(contract_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict:
    return ok({"status": "ok"})
