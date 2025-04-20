from celery import Celery
from src.core.config import settings


app = Celery(
    'tasks', 
    broker=settings.redis_url(0),
    backend=settings.redis_url(0),
    include=['worker.celery_tasks']
)


app.conf.update(
    task_routes={
        'worker.celery_tasks.predict': {'queue': 'video_analysis'},
    },
    task_default_queue='video_analysis',
    task_default_exchange='video_analysis',
    task_default_routing_key='video_analysis',
    task_always_eager=False,
    task_eager_propagates=False,
)




