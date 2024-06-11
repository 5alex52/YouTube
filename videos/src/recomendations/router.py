import uuid
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

from ..exceptions import InvalidTokenException
from ..global_utils import get_user_id
from ..videos.schemas import Video
from .service import UserTagsService

recomendations_router = APIRouter(prefix="/video", tags=["recomendations"])


@recomendations_router.get("/watch/{video_id}")
async def watch(
    request: Request,
    video_id: uuid.UUID,
) -> Video:
    try:
        user_id: uuid.UUID = get_user_id(request)
    except (InvalidTokenException, HTTPException):
        user_id = None
    return await UserTagsService.watch(request, video_id, user_id)


@recomendations_router.get("/recomendations/")
async def get_recomendations(
    request: Request,
) -> List[Video]:
    try:
        user_id: uuid.UUID = get_user_id(request)
    except (InvalidTokenException, HTTPException):
        user_id = None
    return await UserTagsService.get_recomendations(user_id)
