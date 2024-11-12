"""Исполняющий файл проекта."""
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from core.handlers.handler import router, start_bot, stop_bot
from core.database.dataTools import create_tables, delete_tables


logging.basicConfig(
    filename="BotShop.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def start() -> None:
    """
    Функция инициации и запуска бота.

    Notes:

        Входная точка в проект с настройками
        и регистрацией роутеров.
    """
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode='HTML'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация роутера
    dp.include_router(router=router)

    # Регистрация функций для старта и остановки
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await create_tables()
        await dp.start_polling(bot, skip_updates=False)
    except Exception as ex:
        logger.debug(f"Ошибка приложения {ex}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
