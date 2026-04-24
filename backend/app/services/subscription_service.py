from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Subscription
from app.schemas.subscription import SubscriptionUpdate


async def get_subscription(
    db: AsyncSession,
    counselor_id: UUID,
) -> Subscription:
    result = await db.execute(
        select(Subscription).where(Subscription.counselor_id == counselor_id)
    )
    subscription = result.scalar_one_or_none()
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found",
        )
    return subscription


async def update_subscription(
    db: AsyncSession,
    counselor_id: UUID,
    data: SubscriptionUpdate,
) -> Subscription:
    subscription = await get_subscription(db, counselor_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subscription, key, value)
    await db.flush()
    await db.refresh(subscription)
    return subscription
