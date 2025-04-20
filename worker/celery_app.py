from celery import Celery
from src.core.config import settings


app = Celery(
    'tasks', 
    broker=settings.redis_url(0),
    backend=settings.redis_url(0),
    include=['worker.celery_tasks']
)

app.conf.result_backend=settings.redis_url(0)


