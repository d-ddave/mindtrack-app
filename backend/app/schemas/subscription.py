from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    plan: str = "trial"
    razorpay_sub_id: str | None = None
    promo_code: str | None = None


class SubscriptionUpdate(BaseModel):
    plan: str | None = None
    status: str | None = None
    razorpay_sub_id: str | None = None
    current_period_end: datetime | None = None


class SubscriptionResponse(BaseModel):
    id: UUID
    counselor_id: UUID | None = None
    plan: str | None = None
    status: str | None = None
    trial_ends_at: datetime | None = None
    current_period_end: datetime | None = None
    razorpay_sub_id: str | None = None
    promo_code: str | None = None
    discount_pct: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
