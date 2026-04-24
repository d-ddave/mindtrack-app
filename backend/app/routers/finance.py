from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_counselor
from app.models.tables import Counselor
from app.schemas.finance import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services.finance_service import (
    create_transaction,
    get_transaction,
    get_transactions,
    update_transaction,
)

router = APIRouter(prefix="/finance", tags=["finance"])


@router.post("/transactions", response_model=TransactionResponse)
async def create(
    body: TransactionCreate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> TransactionResponse:
    transaction = await create_transaction(db, counselor.id, body)
    return TransactionResponse.model_validate(transaction)


@router.get("/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> list[TransactionResponse]:
    transactions = await get_transactions(db, counselor.id, skip, limit)
    return [TransactionResponse.model_validate(t) for t in transactions]


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_one(
    transaction_id: UUID,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> TransactionResponse:
    transaction = await get_transaction(db, counselor.id, transaction_id)
    return TransactionResponse.model_validate(transaction)


@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update(
    transaction_id: UUID,
    body: TransactionUpdate,
    counselor: Counselor = Depends(get_current_counselor),
    db: AsyncSession = Depends(get_db),
) -> TransactionResponse:
    transaction = await update_transaction(db, counselor.id, transaction_id, body)
    return TransactionResponse.model_validate(transaction)
