"""Модуль обработчиков Aiogram3."""
import os
import logging
from decimal import Decimal, InvalidOperation
from aiogram import Router, Bot, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.dataTools import (get_all_products, get_user, add_user,
                                     add_product, increasing_quantity_of_goods,
                                     get_balance, get_referal_code,
                                     top_up_admin, write_off_admin,
                                     delete_item, add_to_cart, get_user_cart,
                                     item_un_cart, get_user_collection_tools,
                                     add_product_to_users_collection_tools,
                                     empty_the_basket)
from core.payment.payment_tools import check_payment, create_payment
from core.utils.commands import set_commands
from core.contents.content import (bot_status, user_menu,
                                   admin_menu, fsm_product)
from core.keyboards.reply_inline import ReplyKeyBoards, InlineKeyBoards
from core.state_models.state import Product_add, TopUpAdmin, WriteOffAdmin
from core.tools.tool import generate_gift


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
                                                              user_menu[11],
                                                              user_menu[5],
                                                              user_menu[9]))
    else:
        await message.answer(
            f"Привет <b>{message.from_user.first_name}</b>!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(user_menu[1],
                                                              user_menu[2],
                                                              user_menu[3],
                                                              user_menu[11],
                                                              user_menu[5],
                                                              user_menu[9]))


@router.message(F.text == admin_menu[7], F.from_user.id == admin_id)
async def moder_menu(message: Message) -> None:
    """Админ меню."""
    await message.answer(
            f"Привет <b>{message.from_user.first_name}</b>!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(admin_menu[1],
                                                              admin_menu[3],
                                                              admin_menu[4],
                                                              admin_menu[5],
                                                              admin_menu[8]
                                                              ))


@router.message(F.text == admin_menu[8])
async def backward(message: Message) -> None:
    """Обработка кнопки  'НАЗАД' - возвращает в главное меню."""
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer(
            text="Вы в меню!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(
                admin_menu[7],
                user_menu[1],
                user_menu[2],
                user_menu[3],
                user_menu[11],
                user_menu[5],
                user_menu[9],))
    else:
        await message.answer(
            text="Вы в меню!",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(
                user_menu[1],
                user_menu[2],
                user_menu[3],
                user_menu[11],
                user_menu[5],
                user_menu[9]))


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
    price = message.text
    item_price = None
    try:
        value = Decimal(price)
        if -99999999.99 < value < 99999999.99:
            item_price = value
        else:
            await message.answer(fsm_product[15])
            return
    except (ValueError, InvalidOperation):
        await message.answer(fsm_product[14])
        return
    if item_price is not None:
        await state.update_data(price=item_price)
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
    await message.answer(f"Ваш баланс: {str(balance)} р.")


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
    if ref_code != 0:
        await message.answer(f"Ваш реферальный код: {ref_code}")
    else:
        await message.answer(text=ref_code)


@router.message(F.text == user_menu[5])
async def get_contacts(message: Message) -> None:
    """Получение контактов, для связи с операторами и админами."""
    await message.answer(f"Администратор: {user_menu[8]}")


@router.message(F.text == user_menu[9])
async def get_my_id(message: Message) -> None:
    """Получение своего ID."""
    user_id = message.from_user.id
    await message.answer(f"Ваш ID: {user_id}")


@router.message(F.text == admin_menu[3], F.from_user.id == admin_id)
async def make_gift(message: Message) -> None:
    """Генерация рандомного гифт-ключа."""
    gift = await generate_gift()
    await message.answer(F"Вот гифт-ключ: {gift}")


@router.message(F.text == admin_menu[4], F.from_user.id == admin_id)
async def top_up_start(message: Message, state: FSMContext) -> None:
    """Ручное пополнение баланса (FSM). Указание ID пользователя."""
    await state.set_state(TopUpAdmin.user_id)
    await message.answer(fsm_product[7])
    await message.answer(fsm_product[12])


@router.message(TopUpAdmin.user_id, F.from_user.id == admin_id)
async def top_up_user_id(message: Message, state: FSMContext) -> None:
    """Ручное пополнение баланса (FSM). Указание суммы."""
    user = message.text
    if not user.isdigit():
        await message.answer(fsm_product[13])
        return

    await state.update_data(user_id=int(user))
    await state.set_state(TopUpAdmin.amount)
    await message.answer(fsm_product[8])


@router.message(TopUpAdmin.amount, F.from_user.id == admin_id)
async def top_up_amount(message: Message, state: FSMContext) -> None:
    """Ручное пополнение баланса (FSM). Пополнение баланса."""
    user_amount = message.text
    try:
        value = Decimal(user_amount)
    except (ValueError, InvalidOperation):
        await message.answer(fsm_product[14])
        return

    await state.update_data(amount=value)
    data: dict = await state.get_data()
    result = await top_up_admin(user_id=data['user_id'],
                                amount=data['amount'])
    await message.answer(text=result)
    await state.clear()


@router.message(F.text == admin_menu[5], F.from_user.id == admin_id)
async def write_off_start(message: Message, state: FSMContext) -> None:
    """Ручное списание средств (FSM). Указание ID пользователя."""
    await state.set_state(WriteOffAdmin.user_id)
    await message.answer(fsm_product[7])
    await message.answer(fsm_product[12])


@router.message(WriteOffAdmin.user_id, F.from_user.id == admin_id)
async def write_off_user_id(message: Message, state: FSMContext) -> None:
    """Ручное списание средств (FSM). Указание суммы."""
    user = message.text
    if not user.isdigit():
        await message.answer(fsm_product[13])
        return

    await state.update_data(user_id=int(user))
    await state.set_state(WriteOffAdmin.amount)
    await message.answer(fsm_product[11])


@router.message(WriteOffAdmin.amount, F.from_user.id == admin_id)
async def write_off_amount(message: Message, state: FSMContext) -> None:
    """Ручное списание средств (FSM). Списание средств."""
    user_amount = message.text
    try:
        value = Decimal(user_amount)
    except (ValueError, InvalidOperation):
        await message.answer(fsm_product[14])
        return
    await state.update_data(amount=value)
    data: dict = await state.get_data()
    result = await write_off_admin(user_id=data['user_id'],
                                   amount=data['amount'])
    await message.answer(text=result)
    await state.clear()


@router.message(F.text == user_menu[1])
async def catalog(message: Message) -> None:
    """Получение всех товаров в каталоге."""
    user_id = message.from_user.id
    products = await get_all_products()
    if products:
        for item in products:
            text = (
                f"Название: {item['name']}\n"
                f"Описание: {item['description']}\n"
                f"Цена: {item['price']} руб."
            )
            if user_id == admin_id:
                buttons = [
                    (user_menu[6], f"to_cart:{item['id']}"),
                    (admin_menu[2], f"delete_item:{item['id']}")
                ]
                await message.answer_photo(
                    photo=item['photo_id'],
                    caption=text,
                    reply_markup=InlineKeyBoards.create_keyboard_inline(
                        buttons).as_markup())
            else:
                buttons = [
                    (user_menu[6], f"to_cart:{item['id']}")
                    ]
                await message.answer_photo(
                    photo=item['photo_id'],
                    caption=text,
                    reply_markup=InlineKeyBoards.create_keyboard_inline(
                        buttons).as_markup())
    else:
        await message.answer("Товары отсутствуют в базе данных!")


@router.callback_query(F.data.startswith("delete_item:"))
async def delete_one_item(callback: CallbackQuery) -> None:
    """Удаление товара из каталога."""
    item_id = callback.data.split(":")[1]
    result = await delete_item(item_id=int(item_id))
    await callback.message.edit_caption(caption=result)


@router.callback_query(F.data.startswith("to_cart:"))
async def item_to_cart(callback: CallbackQuery) -> None:
    """Добавление товаров в корзину."""
    product_id = callback.data.split(":")[1]
    user_id = callback.from_user.id
    result = await add_to_cart(user_id=user_id,
                               product_id=int(product_id))
    await callback.message.edit_caption(caption=result)


@router.message(F.text == user_menu[2])
async def get_cart(message: Message) -> None:
    """Получение корзины пользователя."""
    user_id = message.from_user.id
    products = await get_user_cart(user_id=user_id)
    if products:
        for product in products:
            text = (
                f"id: {product.id}\n"
                f"Название: {product.product_name}\n"
                f"Описание: {product.description}\n"
                f"Цена: {product.price} рублей."
            )
            buttons = [
                    (user_menu[7], f"un-cart:{product.id}"),
            ]
            await message.answer_photo(
                photo=product.photo_id,
                caption=text,
                reply_markup=InlineKeyBoards.create_keyboard_inline(
                    buttons).as_markup())
        await message.answer(text="Выберите действие...",
                             reply_markup=ReplyKeyBoards.create_keyboard_reply(
                                 user_menu[10],
                                 user_menu[12],
                                 admin_menu[8]
                                 ))
    else:
        await message.answer("Корзина пуста!")


@router.callback_query(F.data.startswith("un-cart:"))
async def un_cart(callback: CallbackQuery) -> None:
    """Удаление товара из корзины."""
    product_id = callback.data.split(":")[1]
    user_id = callback.from_user.id
    result = await item_un_cart(user_id=user_id,
                                product_id=int(product_id))
    await callback.message.edit_caption(caption=result)


@router.message(F.text == user_menu[11])
async def get_user_collection(message: Message) -> None:
    """Получение пользователем его купленных товаров."""
    user_id = message.from_user.id
    products = await get_user_collection_tools(user_id=user_id)
    if products:
        for item in products:
            text = (
                f"Название: {item.product_name}\n"
                f"Цийровой код: {item.product_code}"
            )
            await message.answer_photo(
                photo=item.photo_id,
                caption=text)
    else:
        await message.answer("Вы ещё не купили товары (((")


@router.message(F.text == user_menu[10])
async def balance_payment(message: Message) -> None:
    """Оплата через баланс."""
    user_id = message.from_user.id
    cart_products = await get_user_cart(user_id=user_id)
    user_balance = await get_balance(user_id=user_id)
    amount = 0
    for item in cart_products:
        amount += item.price
    if float(user_balance) >= float(amount):
        for item in cart_products:
            await add_product_to_users_collection_tools(
                user_id=user_id,
                product_name=item.product_name,
                product_code=await generate_gift(),
                photo_id=item.photo_id)
        await empty_the_basket(user_id=user_id)
        await write_off_admin(user_id=user_id, amount=amount)
        await message.answer(
            "Успешно, товары вы найдете в разделе 'МОИ ТОВАРЫ'.")
    else:
        await message.answer("На баалнсе недостаточно средств...")


@router.message(F.text == user_menu[12])
async def card_payment(message: Message) -> None:
    """Оплата картой."""
    user_id = message.chat.id
    cart_products = await get_user_cart(user_id=user_id)
    amount = 0
    for item in cart_products:
        amount += item.price

    pyment_url, payment_id = await create_payment(amount, user_id,
                                                  "Оплата корзины...")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Оплатить",
        url=pyment_url
    ))
    builder.add(types.InlineKeyboardButton(
        text="Проверить оплату",
        callback_data=f"check_{payment_id}"
    ))

    await message.answer("Счёт сформирован...",
                         reply_markup=builder.as_markup())


@router.callback_query(lambda c: 'check' in c.data)
async def check_card_payment(callback: types.CallbackQuery) -> None:
    user_id = callback.message.chat.id
    result = await check_payment(callback.data.split("_")[-1])
    if result:
        cart_products = await get_user_cart(user_id=user_id)
        for item in cart_products:
            await add_product_to_users_collection_tools(
                user_id=user_id,
                product_name=item.product_name,
                product_code=await generate_gift(),
                photo_id=item.photo_id)
        await empty_the_basket(user_id=user_id)
        await callback.message.answer(
            "Успешно, товары вы найдете в разделе 'МОИ ТОВАРЫ'.")
    else:
        await callback.message.answer(
            "Оплата ещё не прошла или возникла ошибка!")
