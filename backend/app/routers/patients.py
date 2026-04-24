from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient_service import (
    create_patient,
    delete_patient,
    get_patient,
    get_patients,
    update_patient,
)

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientResponse)
async def create(
    body: PatientCreate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    patient = await create_patient(db, counselor.id, body)
    return PatientResponse.model_validate(patient)


@router.get("", response_model=list[PatientResponse])
async def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    active_only: bool = Query(True),
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> list[PatientResponse]:
    patients = await get_patients(db, counselor.id, skip, limit, active_only)
    return [PatientResponse.model_validate(p) for p in patients]


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_one(
    patient_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    patient = await get_patient(db, counselor.id, patient_id)
    return PatientResponse.model_validate(patient)


@router.patch("/{patient_id}", response_model=PatientResponse)
async def update(
    patient_id: UUID,
    body: PatientUpdate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    patient = await update_patient(db, counselor.id, patient_id, body)
    return PatientResponse.model_validate(patient)


@router.delete("/{patient_id}", status_code=204)
async def delete(
    patient_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> None:
    await delete_patient(db, counselor.id, patient_id)
