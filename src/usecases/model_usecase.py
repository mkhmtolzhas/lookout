from abc import ABC, abstractmethod
import asyncio
from typing import AsyncGenerator
from src.schemas.model_schema import ModelSchema
from src.schemas.video_schema import VideoCreate
from src.schemas.analysis_result_schema import AnalysisResultCreate, AnalysisResultResponse, AnalysisResultUpdate
from src.core.storage.storage import Storage
from src.core.storage.s3_storage import s3_storage
from src.repo.video_repo import video_repository
from src.repo.analysis_result_repo import analysis_result_repository
from .repository import Repository
from io import BytesIO
from src.inference.model_inference import ModelInference, model_inference



class ModelUseCase(ABC):
    """
    Abstract base class for model use cases.
    """

    @abstractmethod
    async def analyze_video(self, user_id: int, file: BytesIO, file_name: str) -> ModelSchema:
        """
        Analyze the given data and return the result.
        """
        pass


    @abstractmethod
    async def get_result(self, task_id: str) -> ModelSchema:
        """
        Get the analysis result for the given video ID.
        """
        pass


class ModelUseCaseImpl(ModelUseCase):
    """
    Implementation of model use cases.
    """

    def __init__(self, storage: Storage, video_repository: Repository, analysis_result_repository: Repository, model_inference: ModelInference):
        """
        Initialize the model use case with storage and repositories.
        """
        self.storage = storage
        self.video_repository = video_repository
        self.analysis_result_repository = analysis_result_repository
        self.model_inference = model_inference

    
    async def analyze_video(self, user_id: int, file: BytesIO, file_name: str) -> ModelSchema:
        url = await self.storage.upload(file, file_name)
        video = VideoCreate(user_id=user_id, file_url=url)
        await self.video_repository.create(video)
        return await asyncio.to_thread(self.model_inference.analyze_video, url)

    async def get_result(self, task_id: str) -> ModelSchema:
        result = await asyncio.to_thread(self.model_inference.get_result, task_id)
        if not result:
            raise ValueError("Result not found")
        return result
        
        
        

async def get_model_use_case() -> AsyncGenerator[ModelUseCase, None]:
    yield ModelUseCaseImpl(s3_storage, video_repository, analysis_result_repository, model_inference)

