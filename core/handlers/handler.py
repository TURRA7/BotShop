"""Модуль обработчиков Aiogram3."""
import os
import logging
from aiogram import F
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from core.database.dataTools import get_user, add_user
from core.utils.commands import set_commands
from core.contents.content import (bot_status, user_menu,
                                   admin_menu)
from core.keyboards.reply_inline import ReplyKeyBoards


logger = logging.getLogger(__name__)
admin_id = int(os.environ.get("ADMIN_ID"))
router = Router()


async def start_bot(bot: Bot) -> None:
    """Отправляет пользователю сообщение о старте бота."""
    await set_commands(bot)
    await bot.send_message(admin_id, text=bot_status[1])
    logger.info(bot_status[1])


async def stop_bot(bot: Bot) -> None:
    """Отправляет пользователю сообщение об остановке бота."""
    await bot.send_message(admin_id, text=bot_status[2])
    logger.info(bot_status[2])


@router.message(Command("start"))
async def get_start(message: Message) -> None:
    """Обработчик команды /start"""
    user_id = message.from_user.id
    result = await get_user(user_id=user_id)
    if result is None:
        user = await add_user(user_id=user_id)
        await message.answer(text=user)
    if user_id == admin_id:
        await message.answer(
            f"Привет <b>{message.from_user.first_name}</b>!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(admin_menu[7],
                                                              user_menu[1],
                                                              user_menu[2],
                                                              user_menu[3],
                                                              user_menu[4],
                                                              user_menu[5]))
    else:
        await message.answer(
            f"Привет <b>{message.from_user.first_name}</b>!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(user_menu[1],
                                                              user_menu[2],
                                                              user_menu[3],
                                                              user_menu[4],
                                                              user_menu[5]))


@router.message(F.text == admin_menu[7], F.from_user.id == admin_id)
async def admin_menu(message: Message) -> None:
    """Админ меню."""
    await message.answer(
            f"Привет <b>{message.from_user.first_name}</b>!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(admin_menu[1],
                                                              admin_menu[3],
                                                              admin_menu[4],
                                                              admin_menu[5],
                                                              admin_menu[6]
                                                              ))
