from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from src.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentResponse
from .repository import Repository
from src.repo.payment_repo import payment_repository


class PaymentUseCase(ABC):
    """Abstract base class for payment use cases."""
    @abstractmethod
    async def create_payment(self, payment: PaymentCreate) -> PaymentResponse:
        """Create a new payment."""
        pass

    @abstractmethod
    async def get_payment(self, payment_id: int) -> Optional[PaymentResponse]:
        """Retrieve a payment by ID."""
        pass

    @abstractmethod
    async def update_payment(self, payment_id: int, payment: PaymentUpdate) -> PaymentResponse:
        """Update an existing payment."""
        pass

    @abstractmethod
    async def delete_payment(self, payment_id: int) -> bool:
        """Delete a payment by ID."""
        pass

    @abstractmethod
    async def list_payments(self, page: int = 1, limit: int = 10) -> List[PaymentResponse]:
        """List payments with pagination."""
        pass

    @abstractmethod
    async def get_payment_by_fields(self, **kwargs) -> Optional[PaymentResponse]:
        """Retrieve a payment by specific fields."""
        pass

    @abstractmethod
    async def get_payments_by_fields(self, **kwargs) -> Optional[List[PaymentResponse]]:
        """Retrieve payments by specific fields."""
        pass

    


class PaymentUseCaseImpl(PaymentUseCase):
    """Implementation of payment use cases."""

    def __init__(self, repository: Repository):
        self.repository = repository

    async def create_payment(self, payment: PaymentCreate) -> PaymentResponse:
        return await self.repository.create(payment)

    async def get_payment(self, payment_id: int) -> Optional[PaymentResponse]:
        return await self.repository.get(payment_id)

    async def update_payment(self, payment_id: int, payment: PaymentUpdate) -> PaymentResponse:
        return await self.repository.update(payment_id, payment)

    async def delete_payment(self, payment_id: int) -> bool:
        return await self.repository.delete(payment_id)

    async def list_payments(self, page: int = 1, limit: int = 10) -> List[PaymentResponse]:
        return await self.repository.list(limit=limit, offset=(page - 1) * limit)
    
    async def get_payment_by_fields(self, **kwargs) -> Optional[PaymentResponse]:
        return await self.repository.get_by_fields(**kwargs)
    
    async def get_payments_by_fields(self, **kwargs) -> Optional[List[PaymentResponse]]:
        return await self.repository.get_all_by_fields(**kwargs)
    
    
    

async def get_payment_use_case() -> AsyncGenerator[PaymentUseCase, None]:
    """Dependency injection for PaymentUseCase."""
    yield PaymentUseCaseImpl(payment_repository)