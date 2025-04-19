from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from src.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserLogin
from .repository import Repository
from src.repo.user_repo import user_repository
from src.utils.hashing_password import hash_password, verify_password


class UserUseCase(ABC):
    """Abstract base class for user use cases."""

    @abstractmethod
    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Retrieve a user by ID."""
        pass

    @abstractmethod
    async def get_user_by_fields(self, **kwargs) -> Optional[UserResponse]:
        """Retrieve a user by specific fields."""
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
        """Update an existing user."""
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        pass

    @abstractmethod
    async def list_users(self, page: int = 1, limit: int = 10) -> List[UserResponse]:
        """List users with pagination."""
        pass

    @abstractmethod
    async def login_user(self, user: UserLogin) -> Optional[UserResponse]:
        """Login a user."""
        pass
    



class UserUseCaseImpl(UserUseCase):
    """Implementation of user use cases."""

    def __init__(self, repository: Repository):
        self.repository = repository

    async def create_user(self, user: UserCreate) -> UserResponse:
        user.password = hash_password(user.password)
        return await self.repository.create(user)

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        return await self.repository.get(user_id)
    
    async def get_user_by_fields(self, **kwargs) -> Optional[UserResponse]:
        return await self.repository.get_by_fields(**kwargs)

    async def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
        return await self.repository.update(user_id, user)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)

    async def list_users(self, page: int = 1, limit: int = 10) -> List[UserResponse]:
        offset = (page - 1) * limit
        return await self.repository.list(limit=limit, offset=offset)
    
    async def login_user(self, user: UserLogin) -> Optional[UserResponse]:
        user_data = await self.repository.get_by_fields(email=user.email)
        if user_data and verify_password(user.password, user_data.password):
            return user_data
        return None


async def get_user_use_case() -> AsyncGenerator[UserUseCase, None]:
    """Get the user use case."""
    yield UserUseCaseImpl(repository=user_repository)