"""
Модуль с инструментами по созданию Reply и Inline клавиатур.

classes:
    ReplyKeyBoards: Класс для создание Reply клавиатуры.
    InlineKeyBoards: Класс для создание Inline клавиатуры.
"""
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram import types


class ReplyKeyBoards:
    """Класс для работы с Reply клавиатурой."""

    def __init__(self):
        """Метод инициализации класса."""
        pass

    @staticmethod
    def create_keyboard_reply(*buttons: str) -> ReplyKeyboardMarkup:
        """
        Метод создаёт клавиатуру с предаными кнопопками.

        params:
            buttons: кнопки в формате строки: '1_КНОПКА_1'
        """
        kb: list = [[types.KeyboardButton(text=button)] for button in buttons]
        keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
        return keyboard


class InlineKeyBoards:
    """Класс для работы с Inline клавиатурой."""

    def __init__(self) -> None:
        """Метод инициализации класса."""
        pass

    @staticmethod
    def create_keyboard_inline(text, callbacks: str) -> InlineKeyboardMarkup:
        """
        Метод создаёт клавиатуру с предаными кнопопками.

        params:
           callbacks: кнопка в формате: ('название кнопки', 'callback метка').
        """
        links_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=text, callback_data=callbacks),
                ],
            ],
        )
        return links_kb
