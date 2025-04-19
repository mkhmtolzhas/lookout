from contextlib import AbstractAsyncContextManager
from typing import Callable, List, TypeVar, Type

from sqlalchemy import select
from src.schemas.video_schema import VideoCreate, VideoUpdate, VideoResponse
from src.utils.model_adapter import model_to_schema
from src.models.video_model import VideoModel
from src.models.base_model import BaseModel
from src.usecases.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.connections.database.postgres_connection import postgres


T = TypeVar("T", bound=BaseModel)

class VideoRepository(Repository):
    """Repository for video operations."""

    def __init__(self, connection_pool: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]) -> None:
        self.connection_pool = connection_pool
        self.model = model

    async def create(self, obj: VideoCreate) -> VideoResponse:
        """Create a new video."""
        async with self.connection_pool() as session:
            video = self.model(**obj.dict())
            session.add(video)
            await session.commit()
            await session.refresh(video)
            return model_to_schema(video, VideoResponse)
    
    async def get(self, obj_id: int) -> VideoResponse:
        """Retrieve a video by ID."""
        async with self.connection_pool() as session:
            video = await session.get(self.model, obj_id)
            if video:
                return model_to_schema(video, VideoResponse)
            return None
        
    async def update(self, obj_id: int, obj: VideoUpdate) -> VideoResponse:
        """Update an existing video."""
        async with self.connection_pool() as session:
            video = await session.get(self.model, obj_id)
            if video:
                for key, value in obj.dict(exclude_unset=True).items():
                    setattr(video, key, value)
                await session.commit()
                await session.refresh(video)
                return model_to_schema(video, VideoResponse)
            return None
        
    async def delete(self, obj_id: int) -> bool:
        """Delete a video by ID."""
        async with self.connection_pool() as session:
            video = await session.get(self.model, obj_id)
            if video:
                await session.delete(video)
                await session.commit()
                return True
            return False
    
    async def list(self, limit: int, offset: int) -> List[VideoResponse]:
        """List videos with pagination."""
        async with self.connection_pool() as session:
            query = select(self.model).offset(offset).limit(limit)
            result = await session.execute(query)
            videos = result.scalars().all()
            return [model_to_schema(video, VideoResponse) for video in videos]
        
    async def get_by_fields(self, **kwargs) -> List[VideoResponse]:
        """Retrieve a video by specific fields."""
        async with self.connection_pool() as session:
            query = select(self.model).filter_by(**kwargs)
            result = await session.execute(query)
            videos = result.scalars().all()
            return [model_to_schema(video, VideoResponse) for video in videos]
        
video_repository = VideoRepository(postgres.connection_pool_factory(), VideoModel)

