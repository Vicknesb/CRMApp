"""Request timing + slow-query warning middleware (NFR-1)."""
import time
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger()

SLOW_REQUEST_MS = 2000  # SRS §5.1 — 2s page-load budget


class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.1f}"
        if elapsed_ms > SLOW_REQUEST_MS:
            logger.warning("slow_request", path=request.url.path,
                           method=request.method, ms=round(elapsed_ms))
        return response
