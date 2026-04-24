from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


async def create_appointment(
    db: AsyncSession,
    counselor_id: UUID,
    data: AppointmentCreate,
) -> Appointment:
    appointment = Appointment(
        counselor_id=counselor_id,
        patient_id=data.patient_id,
        location_id=data.location_id,
        starts_at=data.starts_at,
        duration_mins=data.duration_mins,
        fee_amount=data.fee_amount,
        fee_currency=data.fee_currency,
    )
    db.add(appointment)
    await db.flush()
    await db.refresh(appointment)
    return appointment


async def get_appointments(
    db: AsyncSession,
    counselor_id: UUID,
    skip: int = 0,
    limit: int = 50,
) -> list[Appointment]:
    result = await db.execute(
        select(Appointment)
        .where(Appointment.counselor_id == counselor_id)
        .order_by(Appointment.starts_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_appointment(
    db: AsyncSession,
    counselor_id: UUID,
    appointment_id: UUID,
) -> Appointment:
    result = await db.execute(
        select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.counselor_id == counselor_id,
        )
    )
    appointment = result.scalar_one_or_none()
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    return appointment


async def update_appointment(
    db: AsyncSession,
    counselor_id: UUID,
    appointment_id: UUID,
    data: AppointmentUpdate,
) -> Appointment:
    appointment = await get_appointment(db, counselor_id, appointment_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(appointment, key, value)
    await db.flush()
    await db.refresh(appointment)
    return appointment


async def delete_appointment(
    db: AsyncSession,
    counselor_id: UUID,
    appointment_id: UUID,
) -> None:
    appointment = await get_appointment(db, counselor_id, appointment_id)
    await db.delete(appointment)
    await db.flush()
