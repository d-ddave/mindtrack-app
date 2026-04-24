import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Counselor(Base):
    __tablename__ = "counselors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    specializations: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )
    fcm_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    referral_code: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)
    referred_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="counselor", cascade="all, delete-orphan"
    )
    patients: Mapped[list["Patient"]] = relationship(
        back_populates="counselor", cascade="all, delete-orphan"
    )
    locations: Mapped[list["Location"]] = relationship(
        back_populates="counselor", cascade="all, delete-orphan"
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="counselor", cascade="all, delete-orphan"
    )
    session_notes: Mapped[list["SessionNote"]] = relationship(
        back_populates="counselor"
    )
    ai_suggestions: Mapped[list["AISuggestion"]] = relationship(
        back_populates="counselor"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="counselor"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id", ondelete="CASCADE"),
        nullable=True,
    )
    plan: Mapped[str | None] = mapped_column(Text, server_default=text("'trial'"))
    status: Mapped[str | None] = mapped_column(Text, server_default=text("'trialing'"))
    trial_ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now() + interval '60 days'"),
    )
    current_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    razorpay_sub_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    promo_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    discount_pct: Mapped[int | None] = mapped_column(Integer, server_default=text("0"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    counselor: Mapped["Counselor"] = relationship(back_populates="subscriptions")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id", ondelete="CASCADE"),
        nullable=True,
    )
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, server_default=text("'{}'::jsonb")
    )
    is_active: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    counselor: Mapped["Counselor"] = relationship(back_populates="patients")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id", ondelete="CASCADE"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )

    counselor: Mapped["Counselor"] = relationship(back_populates="locations")
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="location"
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id", ondelete="CASCADE"),
        nullable=True,
    )
    patient_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id"),
        nullable=True,
    )
    location_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("locations.id"),
        nullable=True,
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_mins: Mapped[int | None] = mapped_column(
        Integer, server_default=text("50")
    )
    status: Mapped[str | None] = mapped_column(
        Text, server_default=text("'scheduled'")
    )
    fee_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fee_currency: Mapped[str | None] = mapped_column(
        Text, server_default=text("'INR'")
    )
    payment_status: Mapped[str | None] = mapped_column(
        Text, server_default=text("'pending'")
    )
    reminder_sent: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    counselor: Mapped["Counselor"] = relationship(back_populates="appointments")
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    location: Mapped["Location"] = relationship(back_populates="appointments")
    session_notes: Mapped[list["SessionNote"]] = relationship(
        back_populates="appointment", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="appointment"
    )


class SessionNote(Base):
    __tablename__ = "session_notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=True,
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id"),
        nullable=True,
    )
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    formatted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(Text, server_default=text("'typed'"))
    therapy_tags: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )
    embedding = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    appointment: Mapped["Appointment"] = relationship(back_populates="session_notes")
    counselor: Mapped["Counselor"] = relationship(back_populates="session_notes")
    attachments: Mapped[list["NoteAttachment"]] = relationship(
        back_populates="session_note", cascade="all, delete-orphan"
    )
    ai_suggestions: Mapped[list["AISuggestion"]] = relationship(
        back_populates="session_note", cascade="all, delete-orphan"
    )


class NoteAttachment(Base):
    __tablename__ = "note_attachments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    session_note_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("session_notes.id", ondelete="CASCADE"),
        nullable=True,
    )
    r2_key: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    ocr_status: Mapped[str | None] = mapped_column(
        Text, server_default=text("'pending'")
    )
    ocr_raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    session_note: Mapped["SessionNote"] = relationship(back_populates="attachments")


class AISuggestion(Base):
    __tablename__ = "ai_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    session_note_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("session_notes.id", ondelete="CASCADE"),
        nullable=True,
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id"),
        nullable=True,
    )
    suggestion_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    therapy_recommended: Mapped[str | None] = mapped_column(Text, nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_used: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    was_applied: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    session_note: Mapped["SessionNote"] = relationship(back_populates="ai_suggestions")
    counselor: Mapped["Counselor"] = relationship(back_populates="ai_suggestions")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    counselor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("counselors.id"),
        nullable=True,
    )
    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id"),
        nullable=True,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str | None] = mapped_column(Text, server_default=text("'INR'"))
    type: Mapped[str | None] = mapped_column(
        Text, server_default=text("'session_fee'")
    )
    payment_mode: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    counselor: Mapped["Counselor"] = relationship(back_populates="transactions")
    appointment: Mapped["Appointment"] = relationship(back_populates="transactions")


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    discount_pct: Mapped[int] = mapped_column(Integer, nullable=False)
    max_uses: Mapped[int | None] = mapped_column(Integer, server_default=text("100"))
    used_count: Mapped[int | None] = mapped_column(Integer, server_default=text("0"))
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_active: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
