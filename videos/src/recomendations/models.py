import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from ..database import Base


class UserTagsModel(Base):
    __tablename__ = "user_tags"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), unique=True)
    tag_views = mapped_column(sa.JSON, nullable=True)

    def __str__(self):
        return self.id
