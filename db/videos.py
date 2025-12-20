from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, DateTime
from typing import List

from db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.video_snapshots import VideoSnapshotsModel


class VideosModel(Base):
    __tablename__ = "videos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    video_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=None,
    )
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=None,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=None,
    )

    snapshots: Mapped[List["VideoSnapshotsModel"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )
