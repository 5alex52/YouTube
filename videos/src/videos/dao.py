from typing import List
from typing import Optional
from typing import Union

from sqlalchemy import delete
from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from ..dao import BaseDAO
from .models import IpModel
from .models import TagModel
from .models import VideoModel
from .schemas import IpBase
from .schemas import TagCreate
from .schemas import TagUpdate
from .schemas import VideoCreate
from .schemas import VideoUpdate


class IpDAO(BaseDAO[IpModel, IpBase, IpBase]):
    model = IpModel


class TagDAO(BaseDAO[TagModel, TagCreate, TagUpdate]):
    model = TagModel


class VideoDAO(BaseDAO[VideoModel, VideoCreate, VideoUpdate]):
    model = VideoModel

    @classmethod
    async def add(cls, session: AsyncSession, obj_in: VideoCreate) -> Optional[VideoModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        tags = [await TagDAO.get_or_create(session, TagCreate(name=tag), name=tag) for tag in update_data["tags"]]
        try:
            obj = cls.model(
                title=update_data["title"],
                tags=tags,
            )

            session.add(obj)
            await session.commit()
            query = (
                select(cls.model)
                .options(selectinload(cls.model.tags), selectinload(cls.model.unique_views))
                .where(cls.model.id == obj.id)
            )

            result = await session.execute(query)
            refreshed_obj = result.scalar()

            return refreshed_obj
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Database Exc: Cannot insert data into table: {e}")
            return None
        except Exception as e:
            await session.rollback()
            print(f"Unknown Exc: Cannot insert data into table: {e}")
            return None

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        *filter,
        offset: int = 0,
        limit: int = 100,
        **filter_by,
    ) -> List[VideoModel]:
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.tags), selectinload(cls.model.unique_views))
            .filter(*filter)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
            .order_by(desc(cls.model.views))
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, *filter, **filter_by) -> Optional[VideoModel]:
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.tags), selectinload(cls.model.unique_views))
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: Union[VideoUpdate, dict],
    ) -> Optional[VideoModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        updated_obj: VideoModel = await cls.find_one_or_none(session, *where)

        non_relationship_update_data = {k: v for k, v in update_data.items() if k not in ["tags", "id", "unique_views"]}
        stmt = update(cls.model).where(*where).values(**non_relationship_update_data)
        await session.execute(stmt)

        updated_obj.tags = []

        if "tags" in update_data:
            updated_obj.tags = [
                await TagDAO.get_or_create(session, TagCreate(name=tag), name=tag) for tag in update_data["tags"]
            ]

        if "unique_views" in update_data:
            updated_obj.unique_views = [
                await IpDAO.get_or_create(session, IpBase(address=ip_address))
                for ip_address in update_data["unique_views"]
            ]

        return updated_obj

    @classmethod
    async def delete(cls, session: AsyncSession, *filter, **filter_by) -> None:
        obj: VideoModel = await cls.find_one_or_none(session, *filter, **filter_by)
        if obj is None:
            raise ValueError
        obj.tags = []
        obj.unique_views = []
        stmt = delete(cls.model).filter(*filter).filter_by(**filter_by)
        await session.execute(stmt)

    @classmethod
    def get_videos_with_tags(cls, session: Session, tags_names: List[str]):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.tags), selectinload(cls.model.unique_views))
            .filter(TagModel.name.in_(tags_names))
            .order_by(desc(cls.model.views))
            .distinct()
        )
        videos = session.execute(query)
        return videos.scalars().all()
