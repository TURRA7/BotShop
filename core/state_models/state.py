"""
Модуль с моделями машины состояний.

Classes:
    Product_add: Добавление продукта
"""
from aiogram.fsm.state import State, StatesGroup


class Product_add(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo_id = State()
