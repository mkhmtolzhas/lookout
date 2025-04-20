from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from src.schemas.analysis_result_schema import AnalysisResultCreate, AnalysisResultUpdate, AnalysisResultResponse
from .repository import Repository
from src.repo.analysis_result_repo import analysis_result_repository



class AnalysisResultUseCase(ABC):
    """Abstract base class for analysis result use cases."""
    @abstractmethod
    async def create_analysis_result(self, analysis_result: AnalysisResultCreate) -> AnalysisResultResponse:
        """Create a new analysis result."""
        pass

    @abstractmethod
    async def get_analysis_result(self, analysis_result_id: int) -> Optional[AnalysisResultResponse]:
        """Retrieve an analysis result by ID."""
        pass

    @abstractmethod
    async def update_analysis_result(self, analysis_result_id: int, analysis_result: AnalysisResultUpdate) -> AnalysisResultResponse:
        """Update an existing analysis result."""
        pass

    @abstractmethod
    async def delete_analysis_result(self, analysis_result_id: int) -> bool:
        """Delete an analysis result by ID."""
        pass

    @abstractmethod
    async def list_analysis_results(self, page: int = 1, limit: int = 10) -> List[AnalysisResultResponse]:
        """List analysis results with pagination."""
        pass

    @abstractmethod
    async def get_analysis_result_by_fields(self, **kwargs) -> Optional[AnalysisResultResponse]:
        """Retrieve an analysis result by specific fields."""
        pass

    @abstractmethod
    async def get_analysis_results_by_fields(self, **kwargs) -> Optional[List[AnalysisResultResponse]]:
        """Retrieve analysis results by specific fields."""
        pass

class AnalysisResultUseCaseImpl(AnalysisResultUseCase):
    """Implementation of analysis result use cases."""

    def __init__(self, repository: Repository):
        self.repository = repository

    async def create_analysis_result(self, analysis_result: AnalysisResultCreate) -> AnalysisResultResponse:
        return await self.repository.create(analysis_result)

    async def get_analysis_result(self, analysis_result_id: int) -> Optional[AnalysisResultResponse]:
        return await self.repository.get(analysis_result_id)

    async def update_analysis_result(self, analysis_result_id: int, analysis_result: AnalysisResultUpdate) -> AnalysisResultResponse:
        return await self.repository.update(analysis_result_id, analysis_result)

    async def delete_analysis_result(self, analysis_result_id: int) -> bool:
        return await self.repository.delete(analysis_result_id)

    async def list_analysis_results(self, page: int = 1, limit: int = 10) -> List[AnalysisResultResponse]:
        return await self.repository.list(limit=limit, offset=(page - 1) * limit)
    
    async def get_analysis_result_by_fields(self, **kwargs) -> Optional[AnalysisResultResponse]:
        return await self.repository.get_by_fields(**kwargs)
    
    async def get_analysis_results_by_fields(self, **kwargs) -> Optional[List[AnalysisResultResponse]]:
        return await self.repository.get_all_by_fields(**kwargs)
    

async def get_analysis_result_use_case() -> AsyncGenerator[AnalysisResultUseCase, None]:
    """Dependency injection for AnalysisResultUseCase."""
    yield AnalysisResultUseCaseImpl(analysis_result_repository)

