from enum import Enum


class LeadStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    UNQUALIFIED = "UNQUALIFIED"
    CONVERTED = "CONVERTED"


class LeadSource(str, Enum):
    WEBSITE = "WEBSITE"
    REFERRAL = "REFERRAL"
    LINKEDIN = "LINKEDIN"
    EMAIL = "EMAIL"
    EVENT = "EVENT"
    COLD = "COLD"
    OTHER = "OTHER"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SALES_MANAGER = "SALES_MANAGER"
    SALES_REP = "SALES_REP"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    FINANCE = "FINANCE"
    MARKETING = "MARKETING"
    READ_ONLY = "READ_ONLY"


class Currency(str, Enum):
    INR = "INR"
    USD = "USD"
