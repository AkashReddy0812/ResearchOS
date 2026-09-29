from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "research_tasks",
    broker=settings.redis.url,
    backend=settings.redis.url,
)

# Autodiscover tasks
celery_app.autodiscover_tasks(["app.tasks"])

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
