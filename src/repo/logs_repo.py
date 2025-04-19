from contextlib import AbstractAsyncContextManager
from typing import Callable, List, TypeVar, Type

from sqlalchemy import select
from src.schemas.logs_schema import LogsCreate, LogsUpdate, LogsResponse
from src.utils.model_adapter import model_to_schema
from src.models.logs_model import LogsModel
from src.models.base_model import BaseModel
from src.usecases.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.connections.database.postgres_connection import postgres


T = TypeVar("T", bound=BaseModel)

class LogsRepository(Repository):
    """Repository for log operations."""

    def __init__(self, connection_pool: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]) -> None:
        self.connection_pool = connection_pool
        self.model = model

    async def create(self, obj: LogsCreate) -> LogsResponse:
        """Create a new log."""
        async with self.connection_pool() as session:
            log = self.model(**obj.dict())
            session.add(log)
            await session.commit()
            await session.refresh(log)
            return model_to_schema(log, LogsResponse)
    
    async def get(self, obj_id: int) -> LogsResponse:
        """Retrieve a log by ID."""
        async with self.connection_pool() as session:
            log = await session.get(self.model, obj_id)
            if log:
                return model_to_schema(log, LogsResponse)
            return None
        
    async def update(self, obj_id: int, obj: LogsUpdate) -> LogsResponse:
        """Update an existing log."""
        async with self.connection_pool() as session:
            log = await session.get(self.model, obj_id)
            if log:
                for key, value in obj.dict(exclude_unset=True).items():
                    setattr(log, key, value)
                await session.commit()
                await session.refresh(log)
                return model_to_schema(log, LogsResponse)
            return None
        
    async def delete(self, obj_id: int) -> bool:
        """Delete a log by ID."""
        async with self.connection_pool() as session:
            log = await session.get(self.model, obj_id)
            if log:
                await session.delete(log)
                await session.commit()
                return True
            return False
    
    async def list(self, limit: int, offset: int) -> List[LogsResponse]:
        """List logs with pagination."""
        async with self.connection_pool() as session:
            query = select(self.model).offset(offset).limit(limit)
            result = await session.execute(query)
            logs = result.scalars().all()
            return [model_to_schema(log, LogsResponse) for log in logs]
        
    async def get_by_fields(self, **kwargs) -> List[LogsResponse]:
        """Retrieve a log by specific fields."""
        async with self.connection_pool() as session:
            query = select(self.model).filter_by(**kwargs)
            result = await session.execute(query)
            logs = result.scalars().first()
            return [model_to_schema(log, LogsResponse) for log in logs]


logs_repository = LogsRepository(postgres.connection_pool_factory(), LogsModel)