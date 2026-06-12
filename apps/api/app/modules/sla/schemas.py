from typing import Optional
from pydantic import BaseModel


class SLAPolicyCreate(BaseModel):
    name: str
    priority: str
    responseMinutes: int
    resolutionMinutes: int
    businessHoursOnly: bool = True


class SLAPolicyUpdate(BaseModel):
    name: Optional[str] = None
    responseMinutes: Optional[int] = None
    resolutionMinutes: Optional[int] = None
    businessHoursOnly: Optional[bool] = None


class EscalationCheck(BaseModel):
    ticketId: str
