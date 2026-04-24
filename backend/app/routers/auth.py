from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor
from app.schemas.auth import AuthResponse, LoginRequest, RefreshResponse, RegisterRequest
from app.schemas.counselor import CounselorResponse, CounselorWithSubscription, SubscriptionInfo
from app.services.auth_service import (
    get_counselor_profile,
    login_counselor,
    refresh_token,
    register_counselor,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    return await register_counselor(
        db=db,
        full_name=body.full_name,
        email=body.email,
        password=body.password,
        referral_code=body.referral_code,
        promo_code=body.promo_code,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    return await login_counselor(
        db=db,
        email=body.email,
        password=body.password,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(
    counselor: Counselor = Depends(get_current_counselor),
) -> RefreshResponse:
    return await refresh_token(str(counselor.id))


@router.get("/me", response_model=CounselorWithSubscription)
async def me(
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> CounselorWithSubscription:
    profile = await get_counselor_profile(db, str(counselor.id))
    sub = profile["subscription"]
    sub_info = None
    if sub:
        sub_info = SubscriptionInfo.model_validate(sub)
    return CounselorWithSubscription(
        id=profile["counselor"].id,
        full_name=profile["counselor"].full_name,
        email=profile["counselor"].email,
        phone=profile["counselor"].phone,
        specializations=profile["counselor"].specializations,
        referral_code=profile["counselor"].referral_code,
        referred_by=profile["counselor"].referred_by,
        created_at=profile["counselor"].created_at,
        updated_at=profile["counselor"].updated_at,
        subscription=sub_info,
    )
