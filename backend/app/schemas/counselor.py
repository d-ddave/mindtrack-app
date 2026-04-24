from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CounselorCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    specializations: list[str] | None = None


class CounselorUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    specializations: list[str] | None = None
    fcm_token: str | None = None


class CounselorResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    phone: str | None = None
    specializations: list[str] | None = None
    referral_code: str | None = None
    referred_by: UUID | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CounselorWithSubscription(CounselorResponse):
    subscription: "SubscriptionInfo | None" = None


class SubscriptionInfo(BaseModel):
    id: UUID
    plan: str | None = None
    status: str | None = None
    trial_ends_at: datetime | None = None
    current_period_end: datetime | None = None
    discount_pct: int | None = None

    model_config = {"from_attributes": True}


CounselorWithSubscription.model_rebuild()
