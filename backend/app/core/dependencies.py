import uuid
from datetime import datetime, timezone

# ── Real JWT imports (kept for when auth is re-enabled) ───────────────────────
from fastapi import Depends, HTTPException, status  # noqa: F401
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # noqa: F401
from sqlalchemy import select  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401

from app.core.database import get_db  # noqa: F401
from app.core.security import verify_access_token  # noqa: F401
from app.models.tables import Counselor

# ── DEV BYPASS: hardcoded mock counselor (no JWT required) ────────────────────
async def get_current_counselor() -> Counselor:
    mock = Counselor()
    mock.id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    mock.full_name = "Dr. Priya Desai"
    mock.email = "priya@mindtrack.in"
    mock.referral_code = "PRIYA001"
    mock.phone = None
    mock.specializations = None
    mock.referred_by = None
    mock.created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mock.updated_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
    return mock
