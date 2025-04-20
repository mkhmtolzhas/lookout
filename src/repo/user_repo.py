from contextlib import AbstractAsyncContextManager
from typing import Callable, List, TypeVar, Type

from sqlalchemy import select
from src.schemas.user_schema import UserCreate, UserInDB, UserUpdate, UserResponse
from src.utils.model_adapter import model_to_schema
from src.models.user_model import UserModel
from src.models.base_model import BaseModel
from src.usecases.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.connections.database.postgres_connection import postgres


T = TypeVar("T", bound=BaseModel)

class UserRepository(Repository):
    """Repository for user operations."""

    def __init__(self, connection_pool: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]) -> None:
        self.connection_pool = connection_pool
        self.model = model

    async def create(self, obj: UserCreate) -> UserResponse:
        """Create a new user."""
        async with self.connection_pool() as session:
            user = self.model(**obj.dict())
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return model_to_schema(user, UserResponse)
    
    async def get(self, obj_id: int) -> UserResponse:
        """Retrieve a user by ID."""
        async with self.connection_pool() as session:
            user = await session.get(self.model, obj_id)
            if user:
                return model_to_schema(user, UserResponse)
            return None
        
    async def update(self, obj_id: int, obj: UserUpdate) -> UserResponse:
        """Update an existing user."""
        async with self.connection_pool() as session:
            user = await session.get(self.model, obj_id)
            if user:
                for key, value in obj.dict(exclude_unset=True).items():
                    setattr(user, key, value)
                await session.commit()
                await session.refresh(user)
                return model_to_schema(user, UserResponse)
            return None
        
    async def delete(self, obj_id: int) -> bool:
        """Delete a user by ID."""
        async with self.connection_pool() as session:
            user = await session.get(self.model, obj_id)
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False
    
    async def list(self, limit: int, offset: int) -> List[UserResponse]:
        """List users with pagination."""
        async with self.connection_pool() as session:
            query = select(self.model).offset(offset).limit(limit)
            result = await session.execute(query)
            users = result.scalars().all()
            return [model_to_schema(user, UserResponse) for user in users]
        
    async def get_by_fields(self, **kwargs) -> UserInDB:
        """Retrieve a user by specific fields."""
        async with self.connection_pool() as session:
            query = select(self.model).filter_by(**kwargs)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                return model_to_schema(user, UserInDB)
            return None
    
    async def get_all_by_fields(self, **kwargs) -> List[UserResponse]:
        """Retrieve a user by specific fields."""
        async with self.connection_pool() as session:
            query = select(self.model).filter_by(**kwargs)
            result = await session.execute(query)
            users = result.scalars().all()
            return [model_to_schema(user, UserResponse) for user in users]

user_repository = UserRepository(postgres.connection_pool_factory(), UserModel)