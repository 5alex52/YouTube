import uuid
from typing import List

from pydantic import BaseModel
from pydantic import Field


class TagBase(BaseModel):
    name: str = Field(None)


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str


class Tag(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class IpBase(BaseModel):
    address: str = Field()


class Ip(IpBase):
    id: int
    address: str


class VideoBase(BaseModel):
    title: str = Field()
    url: str = Field()


class VideoCreate(VideoBase):
    tags: List[str] = []


class VideoUpdate(VideoBase):
    tags: List[str]


class Video(VideoBase):
    id: uuid.UUID
    url: str
    title: str
    views: int
    unique_views: int
    tags: List[str]

    class Config:
        from_attributes = True
