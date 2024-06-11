import uuid
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi import status

from ..global_utils import get_user_id
from .schemas import Tag
from .schemas import TagCreate
from .schemas import TagUpdate
from .schemas import Video
from .schemas import VideoCreate
from .schemas import VideoUpdate
from .service import TagService
from .service import VideoService

tag_router = APIRouter(prefix="/tag", tags=["tag"])
video_router = APIRouter(prefix="/video", tags=["video"])


@tag_router.get("")
async def get_tags_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 25,
    current_user: uuid.UUID = Depends(get_user_id),
) -> List[Tag]:
    return await TagService.get_list(offset=offset, limit=limit)


@tag_router.post("")
async def create_tag(
    tag: TagCreate,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Tag:
    return await TagService.create(tag)


@tag_router.get("/{id}")
async def get_tag(
    id: int,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Tag:
    return await TagService.get(id)


@tag_router.put("/{id}")
async def update_tag(
    id: int,
    tag: TagUpdate,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Tag:
    return await TagService.update(id, tag)


@tag_router.delete("/{id}")
async def delete_tag(
    id: int,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Response:
    await TagService.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@video_router.get("")
async def get_video_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 25,
    current_user: uuid.UUID = Depends(get_user_id),
) -> List[Video]:
    return await VideoService.get_list(offset=offset, limit=limit)


@video_router.post("")
async def create_video(
    request: Request,
    video: VideoCreate,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Video:
    return await VideoService.create(video)


@video_router.get("/{id}")
async def get_video(
    id: uuid.UUID,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Video:
    return await VideoService.get(id)


@video_router.put("/{id}")
async def update_video(
    id: uuid.UUID,
    video: VideoUpdate,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Video:
    return await VideoService.update(id, video)


@video_router.delete("/{id}")
async def delete_video(
    id: uuid.UUID,
    current_user: uuid.UUID = Depends(get_user_id),
) -> Response:
    await VideoService.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
