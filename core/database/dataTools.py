# .scalar_one_or_none()
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from db_models.models import async_session, engine, Base


async def create_tables() -> None:
    """Инициализация таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables() -> None:
    """Удаление таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[Any, Any, None]:
    """Получение асинхронной сессии."""
    async with async_session() as session:
        yield session
