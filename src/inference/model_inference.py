from abc import ABC, abstractmethod
import torch
import torchvision.models as models
from worker.celery_tasks import predict
from celery.result import AsyncResult
from worker.celery_app import app
from src.schemas.model_schema import ModelSchema, ModelResultSchema

class ModelInference(ABC):
    """
    Abstract base class for model inference implementations.
    """

    @abstractmethod
    def analyze_video(self, video_url: str) -> ModelSchema:
        """
        Analyze the given video and return the result.
        """
        pass

    @abstractmethod
    def get_result(self, task_id: str) -> ModelSchema:
        """
        Get the analysis result for the given video ID.
        """
        pass



class ModelInferenceImpl(ModelInference):
    """
    Implementation of model inference.
    """

    def analyze_video(self, video_url: str) -> ModelSchema:

        task = predict.delay(video_url)
        return ModelSchema(status="pending", task_id=str(task.id))


    def get_result(self, task_id: str) -> ModelSchema:
        result = AsyncResult(id=task_id, app=app)

        if result.state == 'PENDING':
            return ModelSchema(status="pending", task_id=task_id)
        elif result.state == 'FAILURE':
            return ModelSchema(status="failed", result=str(result.info), task_id=task_id)
        elif result.state == 'STARTED':
            return ModelSchema(status="processing", task_id=task_id)
        elif result.state == 'SUCCESS':
            return ModelSchema(
                status="success",
                result=ModelResultSchema(**result.result),
                task_id=task_id
            )
        else:
            return ModelSchema(status="error", result=result.info, task_id=task_id)



model_inference = ModelInferenceImpl()