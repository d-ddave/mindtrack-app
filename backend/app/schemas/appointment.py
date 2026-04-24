from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_id: UUID
    location_id: UUID | None = None
    starts_at: datetime
    duration_mins: int = 50
    fee_amount: int | None = None
    fee_currency: str = "INR"


class AppointmentUpdate(BaseModel):
    patient_id: UUID | None = None
    location_id: UUID | None = None
    starts_at: datetime | None = None
    duration_mins: int | None = None
    status: str | None = None
    fee_amount: int | None = None
    fee_currency: str | None = None
    payment_status: str | None = None


class AppointmentResponse(BaseModel):
    id: UUID
    counselor_id: UUID | None = None
    patient_id: UUID | None = None
    location_id: UUID | None = None
    starts_at: datetime
    duration_mins: int | None = None
    status: str | None = None
    fee_amount: int | None = None
    fee_currency: str | None = None
    payment_status: str | None = None
    reminder_sent: bool | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
