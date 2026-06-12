import asyncio
from typing import Any

from app.core.logging import logger


async def record_audit(
    db,
    actor_id: str | None,
    action: str,
    module: str,
    record_id: str | None = None,
    old_values: dict[str, Any] | None = None,
    new_values: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> None:
    """Write an audit log row. Failures are swallowed — never block main op."""
    try:
        await db.auditlog.create(data={
            "userId": actor_id,
            "action": action,
            "module": module,
            "recordId": record_id,
            "oldValues": old_values,
            "newValues": new_values,
            "ipAddress": ip_address,
        })
    except Exception as exc:  # noqa: BLE001
        logger.warning("audit_log_failed", error=str(exc), action=action, module=module)
