from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionNoteCreate(BaseModel):
    appointment_id: UUID
    raw_text: str | None = None
    formatted_text: str | None = None
    source: str = "typed"
    therapy_tags: list[str] | None = None


class SessionNoteUpdate(BaseModel):
    raw_text: str | None = None
    formatted_text: str | None = None
    therapy_tags: list[str] | None = None


class SessionNoteResponse(BaseModel):
    id: UUID
    appointment_id: UUID | None = None
    counselor_id: UUID | None = None
    raw_text: str | None = None
    formatted_text: str | None = None
    source: str | None = None
    therapy_tags: list[str] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NoteAttachmentResponse(BaseModel):
    id: UUID
    session_note_id: UUID | None = None
    r2_key: str
    mime_type: str | None = None
    ocr_status: str | None = None
    ocr_raw_text: str | None = None
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class AISuggestionResponse(BaseModel):
    id: UUID
    session_note_id: UUID | None = None
    counselor_id: UUID | None = None
    suggestion_text: str | None = None
    therapy_recommended: str | None = None
    rationale: str | None = None
    model_used: str | None = None
    confidence: float | None = None
    was_applied: bool | None = None
    generated_at: datetime

    model_config = {"from_attributes": True}
