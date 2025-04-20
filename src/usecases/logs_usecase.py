from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from src.schemas.logs_schema import LogsCreate, LogsUpdate, LogsResponse
from .repository import Repository
from src.repo.logs_repo import logs_repository



class LogsUseCase(ABC):
    """Abstract base class for logs use cases."""
    @abstractmethod
    async def create_log(self, log: LogsCreate) -> LogsResponse:
        """Create a new log entry."""
        pass

    @abstractmethod
    async def get_log(self, log_id: int) -> Optional[LogsResponse]:
        """Retrieve a log entry by ID."""
        pass

    @abstractmethod
    async def update_log(self, log_id: int, log: LogsUpdate) -> LogsResponse:
        """Update an existing log entry."""
        pass

    @abstractmethod
    async def delete_log(self, log_id: int) -> bool:
        """Delete a log entry by ID."""
        pass

    @abstractmethod
    async def list_logs(self, page: int = 1, limit: int = 10) -> List[LogsResponse]:
        """List logs with pagination."""
        pass

    @abstractmethod
    async def get_log_by_fields(self, **kwargs) -> Optional[LogsResponse]:
        """Retrieve a log entry by specific fields."""
        pass

    @abstractmethod
    async def get_logs_by_fields(self, **kwargs) -> Optional[List[LogsResponse]]:
        """Retrieve log entries by specific fields."""
        pass


class LogsUseCaseImpl(LogsUseCase):
    """Implementation of logs use cases."""

    def __init__(self, repository: Repository):
        self.repository = repository

    async def create_log(self, log: LogsCreate) -> LogsResponse:
        return await self.repository.create(log)

    async def get_log(self, log_id: int) -> Optional[LogsResponse]:
        return await self.repository.get(log_id)

    async def update_log(self, log_id: int, log: LogsUpdate) -> LogsResponse:
        return await self.repository.update(log_id, log)

    async def delete_log(self, log_id: int) -> bool:
        return await self.repository.delete(log_id)

    async def list_logs(self, page: int = 1, limit: int = 10) -> List[LogsResponse]:
        return await self.repository.list(limit=limit, offset=(page - 1) * limit)
    
    async def get_log_by_fields(self, **kwargs) -> Optional[LogsResponse]:
        return await self.repository.get_by_fields(**kwargs)
    
    async def get_logs_by_fields(self, **kwargs) -> Optional[List[LogsResponse]]:
        return await self.repository.get_all_by_fields(**kwargs)
    


async def get_logs_use_case() -> AsyncGenerator[LogsUseCase, None]:
    """Dependency injection for LogsUseCase."""
    yield LogsUseCaseImpl(repository=logs_repository)
