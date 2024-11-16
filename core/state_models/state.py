"""
Модуль с моделями машины состояний.

Classes:
    Product_add: Добавление продукта
    TopUpAdmin: Ручное пополнение баланса пользователя
    WriteOffAdmin: Ручное списание средств с баланса пользователя
    TopUP: Пополнение баланса пользователя
"""
from aiogram.fsm.state import State, StatesGroup


class Product_add(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo_id = State()


class TopUpAdmin(StatesGroup):
    user_id = State()
    amount = State()


class WriteOffAdmin(StatesGroup):
    user_id = State()
    amount = State()


class TopUpUser(StatesGroup):
    amount = State()
