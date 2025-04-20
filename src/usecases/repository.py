from typing import Protocol, List
from pydantic import BaseModel


class Repository(Protocol):
    async def create(self, obj: BaseModel) -> BaseModel:
        """Create a new object in the repository."""
        pass

    async def get(self, obj_id: int) -> BaseModel:
        """Retrieve an object by its ID."""
        pass

    async def get_by_fields(self, **kwargs) -> BaseModel:
        """Retrieve an object by specific fields."""
        pass

    async def get_all_by_fields(self, **kwargs) -> List[BaseModel]:
        """Retrieve an object by specific fields."""
        pass

    async def update(self, obj_id: int, obj: BaseModel) -> BaseModel:
        """Update an existing object in the repository."""
        pass

    async def delete(self, obj_id: int) -> bool:
        """Delete an object by its ID."""
        pass

    async def list(self, limit: int, offset: int) -> List[BaseModel]:
        """List objects with pagination."""
        pass
    