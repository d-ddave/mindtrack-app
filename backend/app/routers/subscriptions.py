from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor
from app.schemas.subscription import SubscriptionResponse, SubscriptionUpdate
from app.services.subscription_service import get_subscription, update_subscription

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/me", response_model=SubscriptionResponse)
async def get_my_subscription(
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> SubscriptionResponse:
    subscription = await get_subscription(db, counselor.id)
    return SubscriptionResponse.model_validate(subscription)


@router.patch("/me", response_model=SubscriptionResponse)
async def update_my_subscription(
    body: SubscriptionUpdate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> SubscriptionResponse:
    subscription = await update_subscription(db, counselor.id, body)
    return SubscriptionResponse.model_validate(subscription)
