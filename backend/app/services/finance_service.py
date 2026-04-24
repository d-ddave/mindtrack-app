from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Transaction
from app.schemas.finance import TransactionCreate, TransactionUpdate


async def create_transaction(
    db: AsyncSession,
    counselor_id: UUID,
    data: TransactionCreate,
) -> Transaction:
    transaction = Transaction(
        counselor_id=counselor_id,
        appointment_id=data.appointment_id,
        amount=data.amount,
        currency=data.currency,
        type=data.type,
        payment_mode=data.payment_mode,
        reference_id=data.reference_id,
        paid_at=data.paid_at,
        notes=data.notes,
    )
    db.add(transaction)
    await db.flush()
    await db.refresh(transaction)
    return transaction


async def get_transactions(
    db: AsyncSession,
    counselor_id: UUID,
    skip: int = 0,
    limit: int = 50,
) -> list[Transaction]:
    result = await db.execute(
        select(Transaction)
        .where(Transaction.counselor_id == counselor_id)
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_transaction(
    db: AsyncSession,
    counselor_id: UUID,
    transaction_id: UUID,
) -> Transaction:
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.counselor_id == counselor_id,
        )
    )
    transaction = result.scalar_one_or_none()
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return transaction


async def update_transaction(
    db: AsyncSession,
    counselor_id: UUID,
    transaction_id: UUID,
    data: TransactionUpdate,
) -> Transaction:
    transaction = await get_transaction(db, counselor_id, transaction_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(transaction, key, value)
    await db.flush()
    await db.refresh(transaction)
    return transaction
