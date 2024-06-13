import json
import uuid
from typing import List

from fastapi import Request

from ..celery import generate_recomendations
from ..celery import redis_client
from ..database import async_session_maker
from ..global_utils import get_client_ip
from ..service import BaseService
from ..videos.dao import VideoDAO
from ..videos.models import VideoModel
from ..videos.service import VideoService
from .dao import UserTagsModelDAO
from .schemas import UserTagsCreate
from .schemas import UserTagsUpdate


class UserTagsService(BaseService):
    dao: UserTagsModelDAO = UserTagsModelDAO
    create_chema = UserTagsCreate
    update_chema = UserTagsUpdate

    @classmethod
    async def watch(cls, request: Request, video_id: uuid.UUID, user_id: uuid.UUID | None):
        async with async_session_maker() as session:
            video = await VideoDAO.find_one_or_none(session, id=video_id)
            returned_video = VideoService.video_to_watch_video_schema(video)
            if user_id:
                returned_video.views += 1
                current_ip = get_client_ip(request)
                returned_video.unique_views = [ip.address for ip in video.unique_views]
                if current_ip not in returned_video.unique_views:
                    returned_video.unique_views.append(current_ip)
                returned_video = await VideoService.update(id=video_id, schema=returned_video)
                new_tags = returned_video.tags
                await cls.process_tags(user_id, new_tags)
            return returned_video

    @classmethod
    async def process_tags(cls, user_id: uuid.UUID, new_tags: List[str]):
        user_tags = await cls.get_or_create(cls.create_chema(user_id=user_id))

        if user_tags.tag_views == None:
            user_tags.tag_views = dict()

        for tag in new_tags:
            if str(tag) in user_tags.tag_views:
                user_tags.tag_views[str(tag)] += 1
            else:
                user_tags.tag_views[str(tag)] = 1
        await cls.update(user_tags.id, cls.update_chema(tag_views=user_tags.tag_views))
        generate_recomendations.delay(user_id=user_id, tag_views=user_tags.tag_views)

    @classmethod
    async def get_recomendations(cls, user_id: uuid.UUID | None):
        if user_id:
            key = f"rec_user_{user_id}"
            cached_value = redis_client.get(key)
            if cached_value:
                return [await VideoService.get(video) for video in json.loads(cached_value)]
            await cls.process_tags(user_id, new_tags=[])
        return await VideoService.get_list(offset=0, limit=10)
