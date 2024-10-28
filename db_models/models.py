"""
Работа с базой данных.

Args:
    DB_URI: Данные для подключения к базе PostgreSQL
    engine: Создание асинхронного движка базы данных
    async_session: Конфигуратор асинхронной сессии

Classes:
    Base: Базовый декларотивный класс
    User: Пользователь
    Product: Продукт
    ShoppingCart: Корзина
    Order: Заказ
    OrderItem: Элементы заказа
    Balance: Баланс

Func:
    get_session: Генератор асинхронной сессии
"""
import datetime
from typing import Any, AsyncGenerator
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy import (DECIMAL, Boolean, Column, DateTime,
                        ForeignKey, Integer, String)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager

from config import PG_USER, PG_PASS, PG_HOST, PG_NAME


DB_URI = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{PG_NAME}"
engine = create_async_engine(DB_URI, echo=True)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[Any, Any, None]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    ...


class User(Base):
    """
    Пользователи.

    Args:
        tg_id: ID пользователя в телеграмме
        referal_code: Уникальный реферальный код

        shopping_cart: Связь с таблицей Shopping_cart
        orders: Связь с таблицей Orders
        referred_by: Отметка о том, чей реф. код был задействован
    """
    __tablename__ = "users"

    tg_id = Column(Integer, primary_key=True)
    referal_code = Column(String, unique=True, nullable=False)

    shopping_cart = relationship("ShoppingCart",
                                 back_populates='user',
                                 cascade='all, delete-orphan')
    orders = relationship("Order",
                          back_populates='user',
                          cascade='all, delete-orphan')
    referred_by = Column(Integer, ForeignKey('user.id'), nullable=True)


class Product(Base):
    """
    Продукты.

    Args:
        id: ID продукта в базе данных
        product_name: Название
        description: Описание
        price: Цена
        amount: Количество на складе
        is_stock: Наличие на складе
        photo_id: ID фото в телеграмме
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    is_stock = Column(Boolean, default=True)
    photo_id = Column(String, nullable=False)


class ShoppingCart(Base):
    """
    Корзина.

    Args:
        id: ID корзины
        user_id: ID пользователя корзины
        product_id: ID продукта
        quantity: Количество добавленного продукта

        user: Связь с таблицей User
        product: Связь с таблицей Product
    """
    __tablename__ = 'shopping_cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)

    user = relationship('User', back_populates="shopping_cart")
    product = relationship('Product')


class Order(Base):
    '''
    Заказ.

    Args:
        id: ID заказа
        user_id: ID пользователя корзины
        date_order: Время заказа
        status: Статус заказа
        total_price: Итоговая стоимость заказа

        user: Связь с таблицей User
        order_items: Связь с таблицей OrderItems
    '''
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_order = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')
    total_price = Column(DECIMAL(10, 2), nullable=False)

    user = relationship('User', back_populates="orders")
    order_items = relationship('Order_item',
                               back_populates='order',
                               cascade='all, delete-orphan')


class OrderItem(Base):
    """
    Элементы заказа.

    Args:
        id: ID списка продуктов
        order_id: ID заказа
        product_id: ID продукта
        quantity: Количество добавленного продукта
        price: Цена рподукта

        order: Связь с таблицей Order
        product: Связь с таблицей Product
    """
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product')


class Balance(Base):
    """
    Баланс пользователя.

    Args:
        user_id: ID пользователя баланса
        quantity: Сумма на балансе

        user: Связь с таблицей User
    """
    __tablename__ = 'balances'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    quantity = Column(DECIMAL(10, 2), default=0.0)

    user = relationship('User', back_populates='balance')
