"""
Модуль по работе с меню бота.

function:
    set_commands: Обработчик меню.
"""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    """Обработчик меню (синяя кнопочка слева - снизу)."""
    commands: list = [
        BotCommand(
            command='start',
            description='Начало работы!',
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
