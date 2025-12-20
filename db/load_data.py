import asyncio
from datetime import datetime
import json

from db.base import get_async_db
from db.video_snapshots import VideoSnapshotsModel
from db.videos import VideosModel

with open("videos.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)


async def insert_videos(videos_data: dict = json_data):
    async for db in get_async_db():
        for video_item in videos_data["videos"]:
            # video_copy = video_item.copy()
            # video_copy.pop("snapshots")

            video = VideosModel(
                id=video_item["id"],
                video_created_at=datetime.fromisoformat(
                    video_item["video_created_at"]
                ).replace(tzinfo=None),
                views_count=video_item["views_count"],
                likes_count=video_item["likes_count"],
                reports_count=video_item["reports_count"],
                comments_count=video_item["comments_count"],
                creator_id=video_item["creator_id"],
                created_at=datetime.fromisoformat(video_item["created_at"]).replace(
                    tzinfo=None
                ),
                updated_at=datetime.fromisoformat(video_item["updated_at"]).replace(
                    tzinfo=None
                ),
            )
            db.add(video)

            for snapshot_item in video_item["snapshots"]:
                snapshot = VideoSnapshotsModel(
                    id=snapshot_item["id"],
                    video_id=snapshot_item["video_id"],
                    views_count=snapshot_item["views_count"],
                    likes_count=snapshot_item["likes_count"],
                    reports_count=snapshot_item["reports_count"],
                    comments_count=snapshot_item["comments_count"],
                    delta_views_count=snapshot_item["delta_views_count"],
                    delta_likes_count=snapshot_item["delta_likes_count"],
                    delta_reports_count=snapshot_item["delta_reports_count"],
                    delta_comments_count=snapshot_item["delta_comments_count"],
                    created_at=datetime.fromisoformat(
                        snapshot_item["created_at"]
                    ).replace(tzinfo=None),
                    updated_at=datetime.fromisoformat(
                        snapshot_item["updated_at"]
                    ).replace(tzinfo=None),
                )
                db.add(snapshot)

        await db.flush()
        await db.commit()
        print("🙆 Данные загружены!")


if __name__ == "__main__":
    asyncio.run(insert_videos())
