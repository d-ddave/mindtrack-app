from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor
from app.schemas.note import SessionNoteCreate, SessionNoteResponse, SessionNoteUpdate
from app.services.note_service import (
    create_session_note,
    delete_session_note,
    get_session_note,
    get_session_notes,
    update_session_note,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=SessionNoteResponse)
async def create(
    body: SessionNoteCreate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> SessionNoteResponse:
    note = await create_session_note(db, counselor.id, body)
    return SessionNoteResponse.model_validate(note)


@router.get("", response_model=list[SessionNoteResponse])
async def list_notes(
    appointment_id: UUID | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> list[SessionNoteResponse]:
    notes = await get_session_notes(db, counselor.id, appointment_id, skip, limit)
    return [SessionNoteResponse.model_validate(n) for n in notes]


@router.get("/{note_id}", response_model=SessionNoteResponse)
async def get_one(
    note_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> SessionNoteResponse:
    note = await get_session_note(db, counselor.id, note_id)
    return SessionNoteResponse.model_validate(note)


@router.patch("/{note_id}", response_model=SessionNoteResponse)
async def update(
    note_id: UUID,
    body: SessionNoteUpdate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> SessionNoteResponse:
    note = await update_session_note(db, counselor.id, note_id, body)
    return SessionNoteResponse.model_validate(note)


@router.delete("/{note_id}", status_code=204)
async def delete(
    note_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> None:
    await delete_session_note(db, counselor.id, note_id)
