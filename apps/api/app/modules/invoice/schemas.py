from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.core.enums import InvoiceStatus, Currency, PaymentMethod


class LineItemCreate(BaseModel):
    description: str
    quantity: int = 1
    unitPrice: Decimal
    hsnCode: Optional[str] = None


class LineItemOut(LineItemCreate):
    id: str
    invoiceId: str
    total: Decimal

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: Currency = Currency.INR
    method: PaymentMethod = PaymentMethod.BANK_TRANSFER
    reference: Optional[str] = None
    paidAt: datetime


class PaymentOut(PaymentCreate):
    id: str
    invoiceId: str
    createdAt: datetime

    class Config:
        from_attributes = True


class InvoiceCreate(BaseModel):
    accountId: Optional[str] = None
    contractId: Optional[str] = None
    opportunityId: Optional[str] = None
    issueDate: datetime
    dueDate: datetime
    currency: Currency = Currency.INR
    taxRate: Decimal = Decimal("18")
    notes: Optional[str] = None
    lineItems: List[LineItemCreate]


class InvoiceUpdate(BaseModel):
    status: Optional[InvoiceStatus] = None
    dueDate: Optional[datetime] = None
    notes: Optional[str] = None


class InvoiceOut(BaseModel):
    id: str
    number: str
    status: InvoiceStatus
    accountId: Optional[str] = None
    contractId: Optional[str] = None
    opportunityId: Optional[str] = None
    issueDate: datetime
    dueDate: datetime
    subTotal: Decimal
    taxRate: Decimal
    taxAmount: Decimal
    totalAmount: Decimal
    currency: Currency
    notes: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    lineItems: List[LineItemOut] = []
    payments: List[PaymentOut] = []

    class Config:
        from_attributes = True


class InvoiceListOut(BaseModel):
    id: str
    number: str
    status: InvoiceStatus
    accountId: Optional[str] = None
    totalAmount: Decimal
    currency: Currency
    dueDate: datetime
    createdAt: datetime

    class Config:
        from_attributes = True


class RevenueReport(BaseModel):
    period: str
    totalRevenue: Decimal
    currency: str
    invoiceCount: int


class AgingBucket(BaseModel):
    bucket: str
    totalAmount: Decimal
    invoiceCount: int
