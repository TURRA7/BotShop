"""
Модуль с инструментами по созданию Reply и Inline клавиатур.

classes:
    ReplyKeyBoards: Класс для создание Reply клавиатуры.
    InlineKeyBoards: Класс для создание Inline клавиатуры.
"""
import logging
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


logger = logging.getLogger(__name__)


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

    @staticmethod
    def create_keyboard_inline(buttons) -> InlineKeyboardMarkup:
        """
        Метод создает клавиатуру с заданными кнопками.

        params:
            buttons: список кортежей, где каждый кортеж — это
            ('название кнопки', 'callback метка').

        returns:
            InlineKeyboardMarkup с кнопками.
        """
        builder = InlineKeyboardBuilder()
        for text, callback in buttons:
            builder.row(types.InlineKeyboardButton(
                text=text, callback_data=callback
            ))
        return builder
