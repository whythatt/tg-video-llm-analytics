import asyncio
import os
import httpx
from typing import Optional
from dotenv import load_dotenv

from db.query import execute_sql_query

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

text_for_query = """В бд есть две таблицы:
class VideosModel(Base):
    __tablename__ = "videos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    video_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    snapshots: Mapped[List["VideoSnapshotsModel"]] = relationship(back_populates="video")

class VideoSnapshotsModel(Base):
    __tablename__ = "video_snapshots"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    video_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("videos.id"))
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]
    delta_views_count: Mapped[int]
    delta_likes_count: Mapped[int]
    delta_reports_count: Mapped[int]
    delta_comments_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    video: Mapped["VideosModel"] = relationship(back_populates="snapshots")

приобразуй пользовательский текст в SQL запрос, без пояснений и всего прочего, только запрос, я жду ответ в таком формате: SELECT * FROM users;

пользовательский текст: """


async def query_generation(user_query: str) -> Optional[str]:
    """
    Асинхронный запрос к OpenRouter API.
    Возвращает очищенный ответ или None при ошибке.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {
                "role": "user",
                "content": f"{text_for_query}{user_query}",
            }
        ],
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()  # Вызовет исключение при 4xx/5xx

            query = (
                response.json()["choices"][0]["message"]["content"]
                .replace("`", "")
                .replace("sql", "")
                .strip()
            )
            result = await execute_sql_query(query)
            return result

        except (httpx.RequestError, KeyError, ValueError) as e:
            print(f"Ошибка API: {e}")
            return None


print(
    asyncio.run(
        query_generation(
            "Сколько разных видео получали новые просмотры 27 ноября 2025?"
        )
    )
)
