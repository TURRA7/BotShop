# .scalar_one_or_none()
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from sqlalchemy import select

from db_models.models import (async_session, engine,
                              Base, User, Product)
from tools.tool import generate_code


logger = logging.getLogger(__name__)


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


async def get_user(user_id: int) -> User | None:
    """
    Получение данных о пользователе из таблицы User.

    Args:

        user_id: ID в телеграмме

    Returnes:

        Если пользователь есть в базе, возвращает объект
        пользователя с его данными, иначе None
    """
    async with get_session() as session:
        result = await select(User).where(User.tg_id == user_id)
        user = session.execute(result).scalar_one_or_none()
        return user


async def add_user(user_id: int) -> str | None:
    """
    Добавление пользователя в базу, присвоение реф кода.

    Args:

        user_id: ID в телеграмме

    Returnes:

        Возвращает реферальный код в случае успеха, иначе ошибку.
    """
    async with get_session() as session:
        ref_code = await generate_code(length=8)
        user = User(tg_id=user_id, referal_code=ref_code)
        if (
            isinstance(user, User) and
            user.tg_id and user.referal_code
        ):
            session.add(user)
            await session.commit()
            return ref_code
        else:
            logger.debug(
                "Проблема с добавлением пользователя или генерацией реф кода")
            return "Ошибка нового пользователя!"


async def add_product(name: str, description: str,
                      price: float, photo_id: str) -> str:
    """
    Добавление продукта в базу данных.

    Args:

        name: Название
        description: Описание
        price: Цена
        photo_id: ID фото в телеграмме

    Returnes:

        Добавляет продукт в базу данных, возвращает строку с оповещением
    """
    async with get_session() as session:
        product = Product(product_name=name, description=description,
                          price=price, is_stock=True, photo_id=photo_id)
        if (
            isinstance(product, Product) and
            product.product_name and product.description and
            product.price and product.is_stock and product.photo_id
        ):

            session.add(product)
            await session.commit()
            return "Продукт добавлен!"
        else:
            logger.debug(
                "Проблема с добавлением продукта")
            return "Ошибка нового продукта!"


async def increasing_quantity_of_goods(name: str) -> str:
    """
    Увеличивает количество добавленного товара на 1.

    Args:

        name: Название товара

    Returnes:

        Увеличивает количество товара, возвращает строку с оповещением
    """
    async with get_session() as session:
        result = await select(User).where(Product.product_name == name)
        product = session.execute(result).scalar_one_or_none()
        if isinstance(product, Product):
            product.amount += 1
            await session.commit()
            return True
        else:
            logger.debug(
                "Товраа нет в базе или название передано неверно")
            return False
