from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    appointment_id: UUID | None = None
    amount: int
    currency: str = "INR"
    type: str = "session_fee"
    payment_mode: str | None = None
    reference_id: str | None = None
    paid_at: datetime | None = None
    notes: str | None = None


class TransactionUpdate(BaseModel):
    amount: int | None = None
    payment_mode: str | None = None
    reference_id: str | None = None
    paid_at: datetime | None = None
    notes: str | None = None


class TransactionResponse(BaseModel):
    id: UUID
    counselor_id: UUID | None = None
    appointment_id: UUID | None = None
    amount: int
    currency: str | None = None
    type: str | None = None
    payment_mode: str | None = None
    reference_id: str | None = None
    paid_at: datetime | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
