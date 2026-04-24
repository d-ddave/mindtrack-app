from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


async def create_patient(
    db: AsyncSession,
    counselor_id: UUID,
    data: PatientCreate,
) -> Patient:
    patient = Patient(
        counselor_id=counselor_id,
        full_name=data.full_name,
        age=data.age,
        diagnosis=data.diagnosis,
        contact_info=data.contact_info,
        extra_data=data.extra_data or {},
    )
    db.add(patient)
    await db.flush()
    await db.refresh(patient)
    return patient


async def get_patients(
    db: AsyncSession,
    counselor_id: UUID,
    skip: int = 0,
    limit: int = 50,
    active_only: bool = True,
) -> list[Patient]:
    query = select(Patient).where(Patient.counselor_id == counselor_id)
    if active_only:
        query = query.where(Patient.is_active == True)
    query = query.order_by(Patient.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_patient(
    db: AsyncSession,
    counselor_id: UUID,
    patient_id: UUID,
) -> Patient:
    result = await db.execute(
        select(Patient).where(
            Patient.id == patient_id,
            Patient.counselor_id == counselor_id,
        )
    )
    patient = result.scalar_one_or_none()
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient


async def update_patient(
    db: AsyncSession,
    counselor_id: UUID,
    patient_id: UUID,
    data: PatientUpdate,
) -> Patient:
    patient = await get_patient(db, counselor_id, patient_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(patient, key, value)
    patient.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(patient)
    return patient


async def delete_patient(
    db: AsyncSession,
    counselor_id: UUID,
    patient_id: UUID,
) -> None:
    patient = await get_patient(db, counselor_id, patient_id)
    patient.is_active = False
    patient.updated_at = datetime.now(timezone.utc)
    await db.flush()
