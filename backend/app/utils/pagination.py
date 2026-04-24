from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 50


def get_pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)


class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list
