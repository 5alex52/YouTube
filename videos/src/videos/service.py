import uuid
from typing import Dict, List, Union

from fastapi import HTTPException
from fastapi import status
from ..videos.models import VideoModel

from ..database import async_session_maker
from ..database import sync_session_maker
from ..service import BaseService
from .dao import IpDAO
from .dao import TagDAO
from .dao import VideoDAO
from .schemas import IpBase
from .schemas import TagCreate
from .schemas import TagUpdate
from .schemas import Video
from .schemas import VideoCreate
from .schemas import VideoUpdate


class TagService(BaseService):
    dao: TagDAO = TagDAO
    create_chema = TagCreate
    update_chema = TagUpdate


class IpService(BaseService):
    dao: IpDAO = IpDAO
    create_chema = IpBase
    update_chema = IpBase


class VideoService(BaseService):
    dao: VideoDAO = VideoDAO
    create_chema = VideoCreate
    update_chema = VideoUpdate

    @classmethod
    async def create(cls, schema: create_chema):
        async with async_session_maker() as session:
            db_obj = await cls.dao.add(session, schema)
            if db_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Object creation conflict",
                )
            await session.commit()
        return cls.video_to_watch_video_schema(db_obj)

    @classmethod
    async def get_list(cls, *filter, offset: int = 0, limit: int = 100, **filter_by):
        videos_list = await super().get_list(*filter, offset=offset, limit=limit, **filter_by)
        return [cls.video_to_watch_video_schema(video) for video in videos_list]

    @classmethod
    async def get(cls, id: uuid.UUID):
        video = await super().get(id)
        return cls.video_to_watch_video_schema(video)

    @classmethod
    def video_to_watch_video_schema(cls, video: Video) -> Video:
        """Convert Video object to WatchVideoSchema"""
        return Video(
            id=video.id,
            title=video.title,
            url=video.url,
            views=video.views,
            tags=[tag.name for tag in video.tags],
            unique_views=video.total_views(),
        )

    @classmethod
    async def update(cls, id: uuid.UUID, schema: Union[VideoUpdate, Video, dict]):
        async with async_session_maker() as session:
            db_obj = await cls.dao.update(session, cls.dao.model.id == id, obj_in=schema)
            if db_obj is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
            await session.commit()
        return cls.video_to_watch_video_schema(db_obj)

    @classmethod
    def get_videos_with_tags(cls, tags_names):
        with sync_session_maker() as session:
            videos = cls.dao.get_videos_with_tags(session, tags_names)
        session.commit()
        return videos
    
    @classmethod
    def get_relevant_videos(tag_views: Dict[str, int], videos: List[VideoModel], top_n=10):
        total_views = sum(tag_views.values())
        tag_weights = {tag: count / total_views for tag, count in tag_views.items()}

        # Расчет релевантности для каждого видео
        video_scores = []
        for video in videos:
            score = sum(tag_weights.get(tag.name, 0) for tag in video.tags)
            video_scores.append((str(video.id), score))
            print(f"{str(video.id)} {score}")

        sorted_videos = sorted(video_scores, key=lambda x: x[1], reverse=True)

        return [video_id for video_id, score in sorted_videos[:top_n]]
