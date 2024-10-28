"""Модуль обработчиков Aiogram3."""
import os
import logging
from aiogram import Router, Bot

from core.utils.commands import set_commands
from core.contents.content import bot_status


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
