from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.services.appointment_service import (
    create_appointment,
    delete_appointment,
    get_appointment,
    get_appointments,
    update_appointment,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentResponse)
async def create(
    body: AppointmentCreate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> AppointmentResponse:
    appointment = await create_appointment(db, counselor.id, body)
    return AppointmentResponse.model_validate(appointment)


@router.get("", response_model=list[AppointmentResponse])
async def list_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> list[AppointmentResponse]:
    appointments = await get_appointments(db, counselor.id, skip, limit)
    return [AppointmentResponse.model_validate(a) for a in appointments]


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_one(
    appointment_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> AppointmentResponse:
    appointment = await get_appointment(db, counselor.id, appointment_id)
    return AppointmentResponse.model_validate(appointment)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update(
    appointment_id: UUID,
    body: AppointmentUpdate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> AppointmentResponse:
    appointment = await update_appointment(db, counselor.id, appointment_id, body)
    return AppointmentResponse.model_validate(appointment)


@router.delete("/{appointment_id}", status_code=204)
async def delete(
    appointment_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> None:
    await delete_appointment(db, counselor.id, appointment_id)
