"""
Webhook signature verification + retry logic.
Each provider uses its own verification scheme.
"""
import hashlib
import hmac
import time
from typing import Callable


SUPPORTED_PROVIDERS = {"gmail", "outlook", "slack", "teams", "jira", "azuredevops",
                       "google_calendar", "mailchimp"}


def verify_slack_signature(body: bytes, timestamp: str, signature: str, secret: str) -> bool:
    """Slack uses HMAC-SHA256 over 'v0:{timestamp}:{body}'."""
    if abs(time.time() - float(timestamp)) > 300:
        return False
    base = f"v0:{timestamp}:{body.decode()}"
    expected = "v0=" + hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_github_signature(body: bytes, signature: str, secret: str) -> bool:
    """GitHub/Jira use HMAC-SHA256 with 'sha256=' prefix."""
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_generic_hmac(body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def retry_with_backoff(fn: Callable, max_attempts: int = 3, base_delay: float = 1.0):
    """Retry an async callable with exponential backoff."""
    import asyncio
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return await fn()
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts - 1:
                await asyncio.sleep(base_delay * (2 ** attempt))
    raise last_exc
