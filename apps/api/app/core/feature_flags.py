"""Simple environment-driven feature flags (NFR-9).

Usage:
    from app.core.feature_flags import is_enabled
    if is_enabled("CAMPAIGN_AB_TEST"):
        ...

Flags are read from environment variables prefixed with FEATURE_.
Set FEATURE_<NAME>=true to enable; absent/false = disabled.
"""
import os


def is_enabled(flag: str) -> bool:
    val = os.getenv(f"FEATURE_{flag.upper()}", "false")
    return val.lower() in ("1", "true", "yes", "on")


# Declared flags — document all known flags here
KNOWN_FLAGS = {
    "CAMPAIGN_AB_TEST": "A/B test variant assignment for campaigns",
    "AI_LEAD_SCORING": "GPT-powered lead score enrichment",
    "MOBILE_PUSH": "Web-push notification delivery",
    "ADVANCED_REPORTS": "Custom report builder (guarded by ALLOWED_MODULES)",
    "ESIGN_INTEGRATION": "eSignature provider integration",
}
