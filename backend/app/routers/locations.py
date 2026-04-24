from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor, Location
from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None


class LocationUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    is_active: bool | None = None


class LocationResponse(BaseModel):
    id: UUID
    counselor_id: UUID | None = None
    name: str
    address: str | None = None
    city: str | None = None
    is_active: bool | None = None

    model_config = {"from_attributes": True}


router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("", response_model=LocationResponse)
async def create_location(
    body: LocationCreate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> LocationResponse:
    location = Location(
        counselor_id=counselor.id,
        name=body.name,
        address=body.address,
        city=body.city,
    )
    db.add(location)
    await db.flush()
    await db.refresh(location)
    return LocationResponse.model_validate(location)


@router.get("", response_model=list[LocationResponse])
async def list_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> list[LocationResponse]:
    result = await db.execute(
        select(Location)
        .where(
            Location.counselor_id == counselor.id,
            Location.is_active == True,
        )
        .offset(skip)
        .limit(limit)
    )
    locations = result.scalars().all()
    return [LocationResponse.model_validate(loc) for loc in locations]


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> LocationResponse:
    result = await db.execute(
        select(Location).where(
            Location.id == location_id,
            Location.counselor_id == counselor.id,
        )
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    return LocationResponse.model_validate(location)


@router.patch("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: UUID,
    body: LocationUpdate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> LocationResponse:
    result = await db.execute(
        select(Location).where(
            Location.id == location_id,
            Location.counselor_id == counselor.id,
        )
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(location, key, value)
    await db.flush()
    await db.refresh(location)
    return LocationResponse.model_validate(location)


@router.delete("/{location_id}", status_code=204)
async def delete_location(
    location_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(Location).where(
            Location.id == location_id,
            Location.counselor_id == counselor.id,
        )
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    location.is_active = False
    await db.flush()
