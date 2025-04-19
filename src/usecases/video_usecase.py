from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from src.schemas.video_schema import VideoCreate, VideoUpdate, VideoResponse
from .repository import Repository
from src.repo.video_repo import video_repository


class VideoUseCase(ABC):
    """Abstract base class for video use cases."""
    @abstractmethod
    async def create_video(self, video: VideoCreate) -> VideoResponse:
        """Create a new video."""
        pass

    @abstractmethod
    async def get_video(self, video_id: int) -> Optional[VideoResponse]:
        """Retrieve a video by ID."""
        pass

    @abstractmethod
    async def update_video(self, video_id: int, video: VideoUpdate) -> VideoResponse:
        """Update an existing video."""
        pass

    @abstractmethod
    async def delete_video(self, video_id: int) -> bool:
        """Delete a video by ID."""
        pass

    @abstractmethod
    async def list_videos(self, page: int = 1, limit: int = 10) -> List[VideoResponse]:
        """List videos with pagination."""
        pass

    @abstractmethod
    async def get_video_by_fields(self, **kwargs) -> Optional[VideoResponse]:
        """Retrieve a video by specific fields."""
        pass


class VideoUseCaseImpl(VideoUseCase):
    """Implementation of video use cases."""

    def __init__(self, repository: Repository):
        self.repository = repository

    async def create_video(self, video: VideoCreate) -> VideoResponse:
        return await self.repository.create(video)

    async def get_video(self, video_id: int) -> Optional[VideoResponse]:
        return await self.repository.get(video_id)

    async def update_video(self, video_id: int, video: VideoUpdate) -> VideoResponse:
        return await self.repository.update(video_id, video)

    async def delete_video(self, video_id: int) -> bool:
        return await self.repository.delete(video_id)

    async def list_videos(self, page: int = 1, limit: int = 10) -> List[VideoResponse]:
        return await self.repository.list(limit=limit, offset=(page - 1) * limit)
    
    async def get_video_by_fields(self, **kwargs) -> Optional[VideoResponse]:
        return await self.repository.get_by_fields(**kwargs)


async def get_video_use_case() -> AsyncGenerator[VideoUseCase, None]:
    """Dependency injection for VideoUseCase."""
    yield VideoUseCaseImpl(repository=video_repository)