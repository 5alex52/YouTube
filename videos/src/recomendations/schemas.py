import uuid
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class UserTagsBase(BaseModel):
    tag_views: dict


class UserTagsCreate(BaseModel):
    user_id: uuid.UUID


class UserTagsUpdate(BaseModel):
    tag_views: dict


class UserTags(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    tag_views: dict

    class Config:
        from_attributes = True
