from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey

from db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.videos import VideosModel


class VideoSnapshotsModel(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("videos.id"),
        default=uuid.uuid4,
    )
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]
    delta_views_count: Mapped[int]
    delta_likes_count: Mapped[int]
    delta_reports_count: Mapped[int]
    delta_comments_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=None)
    updated_at: Mapped[datetime] = mapped_column(default=None)

    video: Mapped["VideosModel"] = relationship(back_populates="snapshots")
