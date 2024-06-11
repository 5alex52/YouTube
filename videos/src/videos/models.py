import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class IpModel(Base):
    __tablename__ = "ip"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)

    unique_views = relationship(
        "VideoModel",
        secondary="video_unique_views_association",
        back_populates="unique_views",
    )


class TagModel(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)

    video_tag = relationship("VideoModel", secondary="video_tag_association", back_populates="tags")


video_tag_association_table = sa.Table(
    "video_tag_association",
    Base.metadata,
    sa.Column("video_id", UUID(as_uuid=True), sa.ForeignKey("video.id"), nullable=True),
    sa.Column("tag_id", sa.Integer, sa.ForeignKey("tag.id"), nullable=True),
)

video_unique_views_association_table = sa.Table(
    "video_unique_views_association",
    Base.metadata,
    sa.Column("video_id", UUID(as_uuid=True), sa.ForeignKey("video.id"), nullable=True),
    sa.Column("ip_id", sa.Integer, sa.ForeignKey("ip.id"), nullable=True),
)


class VideoModel(Base):
    __tablename__ = "video"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    views: Mapped[int] = mapped_column(default=0, nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    tags = relationship("TagModel", secondary=video_tag_association_table, back_populates="video_tag")
    unique_views = relationship(
        "IpModel",
        secondary=video_unique_views_association_table,
        back_populates="unique_views",
    )

    def total_views(self):
        return len(self.unique_views)

    def __str__(self):
        return self.title
