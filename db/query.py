from sqlalchemy import text

from db.base import get_async_db


async def execute_sql_query(sql_query: str) -> int:
    async for db in get_async_db():
        result = await db.execute(text(sql_query))
        return result.scalar()
