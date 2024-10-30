"""Модуль обработчиков Aiogram3."""
import os
import logging
from aiogram import F
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.database.dataTools import (get_user, add_user, add_product,
                                     increasing_quantity_of_goods, get_balance,
                                     get_referal_code)
from core.utils.commands import set_commands
from core.contents.content import (bot_status, user_menu,
                                   admin_menu, fsm_product)
from core.keyboards.reply_inline import ReplyKeyBoards
from state_models.state import Product_add


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


@router.message(F.text == admin_menu[1], F.from_user.id == admin_id)
async def add_product_start(message: Message, state: FSMContext) -> None:
    """
    Добавление продукта (FSM) в БД. Указание названия.

    Notes:

        Включает форму Product_add, просит указать название товара
    """
    await state.set_state(Product_add.name)
    await message.answer(fsm_product[1])


@router.message(Product_add.name, F.from_user.id == admin_id)
async def add_product_name(message: Message, state: FSMContext) -> None:
    """
    Добавление продукта (FSM) в БД. Указание описания.

    Notes:

        Фиксирует название товара, переходин к следующему
        состоянию, просит указать описание товара
    """
    await state.update_data(name=message.text)
    await state.set_state(Product_add.description)
    await message.answer(fsm_product[2])


@router.message(Product_add.description, F.from_user.id == admin_id)
async def add_product_desc(message: Message, state: FSMContext) -> None:
    """
    Добавление продукта (FSM) в БД. Указание цены.

    Notes:

        Фиксирует описание товара, переходин к следующему
        состоянию, просит указать цену товара
    """
    await state.update_data(description=message.text)
    await state.set_state(Product_add.price)
    await message.answer(fsm_product[3])


@router.message(Product_add.price, F.from_user.id == admin_id)
async def add_product_price(message: Message, state: FSMContext) -> None:
    """
    Добавление продукта (FSM) в БД. Добавление фото.

    Notes:

        Фиксирует цену товара, переходин к следующему
        состоянию, просит добавить фото
    """
    await state.update_data(price=message.text)
    await state.set_state(Product_add.photo_id)
    await message.answer(fsm_product[4])


@router.message(Product_add.photo_id, F.from_user.id == admin_id)
async def add_product_photo_db(message: Message, state: FSMContext) -> None:
    """
    Добавление продукта (FSM) в БД. Финальный шаг.

    Notes:

        Получает ID фото с системе, собирает данные из машины состояний,
        добавляет товар в базу, увеличивает кол-во товара на 'складе'(в базе),
        возвращает сообщение об успехе или ошибке добавления
    """
    file_id = message.photo[-1].file_id
    data: dict = await state.get_data()
    result = await add_product(name=data['name'],
                               description=data['description'],
                               price=data['price'],
                               photo_id=file_id)
    amount = await increasing_quantity_of_goods(name=data['name'])
    if amount:
        await message.answer(text=result)
        await state.clear()
    else:
        await message.answer(text=fsm_product[6])
        await state.clear()


@router.message(F.text == user_menu[3])
async def get_user_balance(message: Message) -> None:
    """Получение баланса пользователя."""
    user_id = message.from_user.id
    balance = await get_balance(user_id=user_id)
    if isinstance(balance, float):
        await message.answer(f"Ваш баланс: {balance}")
    else:
        await message.answer(text=balance)


@router.message(F.text == user_menu[4])
async def get_referal(message: Message) -> None:
    """
    Получение реферального кода, просмотр рефералов.

    Notes:

        Сейчас добавленно только получение реферального кода,
        в будущем следует добавить ещё и список рефералов.
    """
    user_id = message.from_user.id
    ref_code = await get_referal_code(user_id=user_id)
    await message.answer(text=ref_code)
