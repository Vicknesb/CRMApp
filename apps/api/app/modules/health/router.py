"""Health & readiness endpoints (NFR-3)."""
from fastapi import APIRouter, Depends
from prisma import Prisma
from app.db.client import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness():
    """Kubernetes liveness probe — always 200 if process is up."""
    return {"status": "ok"}


@router.get("/ready")
async def readiness(db: Prisma = Depends(get_db)):
    """Readiness probe — checks DB connectivity."""
    try:
        await db.execute_raw("SELECT 1")
        return {"status": "ready", "db": "ok"}
    except Exception as exc:
        return {"status": "not_ready", "db": str(exc)}, 503


@router.get("/metrics")
async def metrics(db: Prisma = Depends(get_db)):
    """Basic operational metrics for monitoring."""
    lead_count = await db.lead.count()
    ticket_count = await db.ticket.count()
    return {
        "status": "ok",
        "counts": {
            "leads": lead_count,
            "tickets": ticket_count,
        },
    }
