import json
import uuid
from typing import Dict
from typing import List

from .constants import TIMEOUT_REDIS
import redis
from celery import Celery
from celery import shared_task

from .config import settings
from .videos.models import VideoModel
from .videos.service import VideoService


celery_app = Celery(
    "tasks",
    broker=f"pyamqp://{settings.RABBIT_USER}:{settings.RABBIT_PASSWORD}@{settings.RABBIT_HOST}:{settings.RABBIT_PORT}//",
    backend="rpc://",
)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)





@shared_task(name="get_recomenadations")
def generate_recomendations(user_id: uuid.UUID, tag_views: Dict[str, int]):
    videos_with_tags = VideoService.get_videos_with_tags(tag_views.keys())

    videos_ids = VideoService.get_relevant_videos(tag_views, videos_with_tags)

    key = f"rec_user_{user_id}"
    redis_client.setex(key, TIMEOUT_REDIS, json.dumps(videos_ids))
