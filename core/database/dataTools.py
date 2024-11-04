# .scalar_one_or_none()
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from sqlalchemy import select

from core.db_models.models import (async_session, engine,
                                   Base, User, Product, Balance,
                                   ShoppingCart)
from core.tools.tool import generate_code


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
async def get_session() -> AsyncGenerator[Any, Any]:
    """Получение асинхронной сессии."""
    async with async_session() as session:
        yield session


async def get_user(user_id: int) -> User | None:
    """
    Получение данных о пользователе из таблицы User.

    Args:

        user_id: ID в телеграмме

    Returns:

        Если пользователь есть в базе, возвращает объект
        пользователя с его данными, иначе None
    """
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == user_id))
        return result.scalar_one_or_none()


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
        balance = Balance(user_id=user_id, quantity=0.0)
        if (
            isinstance(user, User) and
            user.tg_id and user.referal_code
        ):
            session.add_all([user, balance])
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
        products = await session.execute(
            select(Product).where(Product.product_name == name))
        product = products.scalar_one_or_none()
        if isinstance(product, Product):
            product.amount += 1
            await session.commit()
            return True
        else:
            logger.debug(
                "Товраа нет в базе или название передано неверно")
            return False


async def get_balance(user_id: int) -> float | str:
    """
    Получение баланса пользователя.

    Args:

        user_id: ID пользователя

    Returnes:

        Возвращает баланс пользователя
    """
    async with get_session() as session:
        balances = await session.execute(
            select(Balance).where(Balance.user_id == user_id))
        balance = balances.scalar_one_or_none()
        if isinstance(balance, Balance):
            return balance.quantity
        else:
            logger.debug("Ошибка получения баланса!")
            return "Ошибка получения баланса!"


async def get_referal_code(user_id: int) -> str | int:
    """
    Получение реферального кода.

    Args:

        user_id: ID пользователя

    Returnes:

        Возвращает реферальный код
    """
    async with get_session() as session:
        ref_code = await session.execute(
            select(User).where(User.tg_id == user_id))
        code = ref_code.scalar_one_or_none()
        if isinstance(code, User):
            return code.referal_code
        else:
            logger.debug("Ошибка получения реферального кода!")
            return 0


async def top_up_admin(user_id: int, amount: float) -> str:
    """
    Ручное пополнение баланса пользователя.

    Args:

        user_id: ID пользователя
        amount: Сумма на которую будет увеличен баланс
    """
    async with get_session() as session:
        balances = await session.execute(
            select(Balance).where(Balance.user_id == user_id))
        balance = balances.scalar_one_or_none()
        if isinstance(balance, Balance):
            balance.quantity += amount
            await session.commit()
            return "Баланс пополнен!"
        else:
            logger.debug(
                "Пользователя нет в базе или был передан неверный ID")
            return "Пользователя нет в базе или был передан неверный ID"


async def write_off_admin(user_id: int, amount: float) -> str:
    """
    Ручное списание средств с баланса пользователя.

    Args:

        user_id: ID пользователя
        amount: Сумма на которую будет уменьшен баланс
    """
    async with get_session() as session:
        balances = await session.execute(
            select(Balance).where(Balance.user_id == user_id))
        balance = balances.scalar_one_or_none()
        if isinstance(balance, Balance):
            if balance >= amount:
                balance.quantity -= amount
                await session.commit()
                return "Сумма списанна с баланса!"
            else:
                return "У пользователя нехвататет средств для списания!"
        else:
            return "Пользователя нет в базе или был передан неверный ID"


async def get_all_products() -> list[dict[str, Any]]:
    """
    Получение всех продуктов из базы данных.

    Returns:
        Возвращает список словарей, каждый словарь сожержит
        информацию об одном конкретном товаре.
    """
    async with get_session() as session:
        result = await session.execute(select(Product))
        product = result.scalars().all()
        products = [{"id": item.id,
                     "name": item.product_name,
                     "description": item.description,
                     "price": item.price,
                     "amount": item.amount,
                     "is_stock": item.is_stock,
                     "photo_id": item.photo_id} for item in product]
        return products


async def delete_item(item_id: int) -> str:
    """
    Удаление конкретного товара.

    Args:
        item_id: ID товара

    Returns:
        Удаляет товар из базы данных по переданному ID,
        возвращает строку с оповещением: успех/провал операции
    """
    async with get_session() as session:
        results = await session.execute(
            select(Product).where(Product.id == item_id))
        result = results.scalar_one_or_none()
        if isinstance(result, Product):
            await session.delete(result)
            await session.commit()
            return "Товар удалён!"
        else:
            logger.debug("Ошибка удаления товара!")
            return "Ошибка удаления товара!"


async def add_to_cart(user_id: int, product_id: int) -> str:
    """
    Добавление товаров в корзину.

    Args:
        user_id: ID пользователя
        product_id: ID продукта

    Returns:
        Добавляет продукт в корзину, возвращает строку
        с оповещением
    """
    async with get_session() as session:
        item = ShoppingCart(user_id=user_id,
                            product_id=product_id)
        if (
            isinstance(item, ShoppingCart) and
            item.user_id and item.product_id
        ):
            session.add(item)
            await session.commit()
            return "Продукт добавлен в корзину!"
        else:
            logger.debug(
                "Проблема с добавлением продукта")
            return "Ошибка продукта или корзины!"


async def get_user_cart(user_id: int) -> Product:
    """
    Получение корзины пользователя.

    Args:
        user_id: ID пользователя

    Returns:
        Возвращает список продуктов, добавленных
        конкретным пользователем
    """
    async with get_session() as session:
        request = (
            select(Product)
            .join(ShoppingCart, Product.id == ShoppingCart.product_id)
            .where(ShoppingCart.user_id == user_id)
        )
        results = await session.execute(request)
        result = results.scalars().all()
        return result
