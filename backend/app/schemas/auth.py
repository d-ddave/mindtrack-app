from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    referral_code: str | None = None
    promo_code: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CounselorBrief(BaseModel):
    id: UUID
    full_name: str
    email: str
    referral_code: str | None = None

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    counselor: CounselorBrief


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
