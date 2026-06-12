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


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING = "WAITING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class TicketChannel(str, Enum):
    EMAIL = "EMAIL"
    PORTAL = "PORTAL"
    PHONE = "PHONE"
    MANUAL = "MANUAL"
    CHAT = "CHAT"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActivityType(str, Enum):
    EMAIL = "EMAIL"
    CALL = "CALL"
    MEETING = "MEETING"
    NOTE = "NOTE"
    TASK = "TASK"


class TaskStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
