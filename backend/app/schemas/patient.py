from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PatientCreate(BaseModel):
    full_name: str
    age: int | None = None
    diagnosis: str | None = None
    contact_info: str | None = None
    extra_data: dict | None = None


class PatientUpdate(BaseModel):
    full_name: str | None = None
    age: int | None = None
    diagnosis: str | None = None
    contact_info: str | None = None
    extra_data: dict | None = None
    is_active: bool | None = None


class PatientResponse(BaseModel):
    id: UUID
    counselor_id: UUID | None = None
    full_name: str
    age: int | None = None
    diagnosis: str | None = None
    contact_info: str | None = None
    extra_data: dict | None = None
    is_active: bool | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
