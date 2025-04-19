from contextlib import AbstractAsyncContextManager
from typing import Callable, List, TypeVar, Type

from sqlalchemy import select
from src.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentResponse
from src.utils.model_adapter import model_to_schema
from src.models.payment_model import PaymentModel
from src.models.base_model import BaseModel
from src.usecases.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.connections.database.postgres_connection import postgres


T = TypeVar("T", bound=BaseModel)

class PaymentRepository(Repository):
    """Repository for payment operations."""

    def __init__(self, connection_pool: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]) -> None:
        self.connection_pool = connection_pool
        self.model = model

    async def create(self, obj: PaymentCreate) -> PaymentResponse:
        """Create a new payment."""
        async with self.connection_pool() as session:
            payment = self.model(**obj.dict())
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return model_to_schema(payment, PaymentResponse)
    
    async def get(self, obj_id: int) -> PaymentResponse:
        """Retrieve a payment by ID."""
        async with self.connection_pool() as session:
            payment = await session.get(self.model, obj_id)
            if payment:
                return model_to_schema(payment, PaymentResponse)
            return None
        
    async def update(self, obj_id: int, obj: PaymentUpdate) -> PaymentResponse:
        """Update an existing payment."""
        async with self.connection_pool() as session:
            payment = await session.get(self.model, obj_id)
            if payment:
                for key, value in obj.dict(exclude_unset=True).items():
                    setattr(payment, key, value)
                await session.commit()
                await session.refresh(payment)
                return model_to_schema(payment, PaymentResponse)
            return None
        
    async def delete(self, obj_id: int) -> bool:
        """Delete a payment by ID."""
        async with self.connection_pool() as session:
            payment = await session.get(self.model, obj_id)
            if payment:
                await session.delete(payment)
                await session.commit()
                return True
            return False
    
    async def list(self, limit: int, offset: int) -> List[PaymentResponse]:
        """List payments with pagination."""
        async with self.connection_pool() as session:
            query = select(self.model).offset(offset).limit(limit)
            result = await session.execute(query)
            payments = result.scalars().all()
            return [model_to_schema(payment, PaymentResponse) for payment in payments]
        
    async def get_by_fields(self, **kwargs) -> PaymentResponse:
        """Retrieve a payment by specific fields."""
        async with self.connection_pool() as session:
            query = select(self.model).filter_by(**kwargs)
            result = await session.execute(query)
            payment = result.scalars().first()
            if payment:
                return model_to_schema(payment, PaymentResponse)
            return None


payment_repository = PaymentRepository(postgres.connection_pool_factory(), PaymentModel)