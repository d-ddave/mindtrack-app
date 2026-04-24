import secrets
import string
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.tables import Counselor, PromoCode, Subscription
from app.schemas.auth import AuthResponse, CounselorBrief, RefreshResponse


def _generate_referral_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


async def register_counselor(
    db: AsyncSession,
    full_name: str,
    email: str,
    password: str,
    referral_code: str | None = None,
    promo_code: str | None = None,
) -> AuthResponse:
    existing = await db.execute(select(Counselor).where(Counselor.email == email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    referred_by_id = None
    if referral_code:
        referrer = await db.execute(
            select(Counselor).where(Counselor.referral_code == referral_code)
        )
        referrer_row = referrer.scalar_one_or_none()
        if referrer_row is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid referral code",
            )
        referred_by_id = referrer_row.id

    discount_pct = 0
    promo_code_value = None
    if promo_code:
        promo = await db.execute(
            select(PromoCode).where(
                PromoCode.code == promo_code,
                PromoCode.is_active == True,
            )
        )
        promo_row = promo.scalar_one_or_none()
        if promo_row is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired promo code",
            )
        now = datetime.now(timezone.utc)
        if promo_row.expires_at and promo_row.expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Promo code has expired",
            )
        if promo_row.used_count >= promo_row.max_uses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Promo code usage limit reached",
            )
        discount_pct = promo_row.discount_pct
        promo_code_value = promo_row.code
        await db.execute(
            update(PromoCode)
            .where(PromoCode.id == promo_row.id)
            .values(used_count=promo_row.used_count + 1)
        )

    unique_code = _generate_referral_code()
    while True:
        check = await db.execute(
            select(Counselor).where(Counselor.referral_code == unique_code)
        )
        if check.scalar_one_or_none() is None:
            break
        unique_code = _generate_referral_code()

    counselor = Counselor(
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        referral_code=unique_code,
        referred_by=referred_by_id,
    )
    db.add(counselor)
    await db.flush()

    subscription = Subscription(
        counselor_id=counselor.id,
        promo_code=promo_code_value,
        discount_pct=discount_pct,
    )
    db.add(subscription)
    await db.flush()

    access_token = create_access_token({"sub": str(counselor.id)})

    return AuthResponse(
        access_token=access_token,
        counselor=CounselorBrief(
            id=counselor.id,
            full_name=counselor.full_name,
            email=counselor.email,
            referral_code=counselor.referral_code,
        ),
    )


async def login_counselor(
    db: AsyncSession,
    email: str,
    password: str,
) -> AuthResponse:
    result = await db.execute(select(Counselor).where(Counselor.email == email))
    counselor = result.scalar_one_or_none()

    if counselor is None or not verify_password(password, counselor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": str(counselor.id)})

    return AuthResponse(
        access_token=access_token,
        counselor=CounselorBrief(
            id=counselor.id,
            full_name=counselor.full_name,
            email=counselor.email,
            referral_code=counselor.referral_code,
        ),
    )


async def refresh_token(counselor_id: str) -> RefreshResponse:
    access_token = create_access_token({"sub": counselor_id})
    return RefreshResponse(access_token=access_token)


async def get_counselor_profile(
    db: AsyncSession,
    counselor_id: str,
) -> dict:
    result = await db.execute(
        select(Counselor).where(Counselor.id == counselor_id)
    )
    counselor = result.scalar_one_or_none()
    if counselor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counselor not found",
        )

    sub_result = await db.execute(
        select(Subscription).where(Subscription.counselor_id == counselor.id)
    )
    subscription = sub_result.scalar_one_or_none()

    return {
        "counselor": counselor,
        "subscription": subscription,
    }
