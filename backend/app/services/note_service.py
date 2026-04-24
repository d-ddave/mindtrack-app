from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import SessionNote
from app.schemas.note import SessionNoteCreate, SessionNoteUpdate


async def create_session_note(
    db: AsyncSession,
    counselor_id: UUID,
    data: SessionNoteCreate,
) -> SessionNote:
    note = SessionNote(
        appointment_id=data.appointment_id,
        counselor_id=counselor_id,
        raw_text=data.raw_text,
        formatted_text=data.formatted_text,
        source=data.source,
        therapy_tags=data.therapy_tags,
    )
    db.add(note)
    await db.flush()
    await db.refresh(note)
    return note


async def get_session_notes(
    db: AsyncSession,
    counselor_id: UUID,
    appointment_id: UUID | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[SessionNote]:
    query = select(SessionNote).where(SessionNote.counselor_id == counselor_id)
    if appointment_id:
        query = query.where(SessionNote.appointment_id == appointment_id)
    query = query.order_by(SessionNote.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_session_note(
    db: AsyncSession,
    counselor_id: UUID,
    note_id: UUID,
) -> SessionNote:
    result = await db.execute(
        select(SessionNote).where(
            SessionNote.id == note_id,
            SessionNote.counselor_id == counselor_id,
        )
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session note not found",
        )
    return note


async def update_session_note(
    db: AsyncSession,
    counselor_id: UUID,
    note_id: UUID,
    data: SessionNoteUpdate,
) -> SessionNote:
    note = await get_session_note(db, counselor_id, note_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    note.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(note)
    return note


async def delete_session_note(
    db: AsyncSession,
    counselor_id: UUID,
    note_id: UUID,
) -> None:
    note = await get_session_note(db, counselor_id, note_id)
    await db.delete(note)
    await db.flush()
