from app.core.enums import UserRole

# ── Ability Matrix ────────────────────────────────────────────────────────────
# Format: {module: {action: [allowed_roles]}}
ABILITY_MAP: dict[str, dict[str, list[UserRole]]] = {
    "leads": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP, UserRole.MARKETING],
        "create": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP, UserRole.MARKETING],
        "update": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "delete": [UserRole.ADMIN, UserRole.SALES_MANAGER],
    },
    "contacts": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP, UserRole.SUPPORT_AGENT],
        "create": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "update": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "delete": [UserRole.ADMIN, UserRole.SALES_MANAGER],
    },
    "accounts": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP, UserRole.SUPPORT_AGENT, UserRole.PROJECT_MANAGER, UserRole.FINANCE],
        "create": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "update": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "delete": [UserRole.ADMIN, UserRole.SALES_MANAGER],
    },
    "opportunities": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "create": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "update": [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SALES_REP],
        "delete": [UserRole.ADMIN, UserRole.SALES_MANAGER],
    },
    "tickets": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.SUPPORT_AGENT, UserRole.PROJECT_MANAGER],
        "create": [UserRole.ADMIN, UserRole.SUPPORT_AGENT],
        "update": [UserRole.ADMIN, UserRole.SUPPORT_AGENT],
        "delete": [UserRole.ADMIN],
    },
    "projects": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.PROJECT_MANAGER, UserRole.SUPPORT_AGENT],
        "create": [UserRole.ADMIN, UserRole.PROJECT_MANAGER, UserRole.SALES_MANAGER],
        "update": [UserRole.ADMIN, UserRole.PROJECT_MANAGER],
        "delete": [UserRole.ADMIN],
    },
    "contracts": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.FINANCE],
        "create": [UserRole.ADMIN, UserRole.SALES_MANAGER],
        "update": [UserRole.ADMIN, UserRole.SALES_MANAGER],
        "delete": [UserRole.ADMIN],
    },
    "invoices": {
        "read":   [UserRole.ADMIN, UserRole.FINANCE, UserRole.SALES_MANAGER],
        "create": [UserRole.ADMIN, UserRole.FINANCE],
        "update": [UserRole.ADMIN, UserRole.FINANCE],
        "delete": [UserRole.ADMIN],
    },
    "campaigns": {
        "read":   [UserRole.ADMIN, UserRole.MARKETING, UserRole.SALES_MANAGER],
        "create": [UserRole.ADMIN, UserRole.MARKETING],
        "update": [UserRole.ADMIN, UserRole.MARKETING],
        "delete": [UserRole.ADMIN, UserRole.MARKETING],
    },
    "analytics": {
        "read":   [UserRole.ADMIN, UserRole.SALES_MANAGER, UserRole.FINANCE, UserRole.MARKETING],
    },
    "admin": {
        "read":   [UserRole.ADMIN],
        "create": [UserRole.ADMIN],
        "update": [UserRole.ADMIN],
        "delete": [UserRole.ADMIN],
    },
}

# ── Field-level redaction rules ───────────────────────────────────────────────
# Fields hidden from specific roles
FIELD_REDACTION: dict[str, dict[UserRole, list[str]]] = {
    "leads": {
        UserRole.SALES_REP: ["score", "utmSource", "utmMedium", "utmCampaign"],
        UserRole.MARKETING: [],
    },
    "opportunities": {
        UserRole.SALES_REP: [],
    },
    "invoices": {
        UserRole.SALES_REP: ["subTotal", "taxAmount", "totalAmount"],
        UserRole.SALES_MANAGER: [],
    },
}


def can(role: UserRole, module: str, action: str) -> bool:
    """Return True if the given role can perform action on module."""
    allowed = ABILITY_MAP.get(module, {}).get(action, [])
    return role in allowed or role == UserRole.ADMIN


def redact_fields(data: dict, module: str, role: UserRole) -> dict:
    """Remove fields the role cannot see."""
    hidden = FIELD_REDACTION.get(module, {}).get(role, [])
    return {k: v for k, v in data.items() if k not in hidden}
