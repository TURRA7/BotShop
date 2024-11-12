from sqlalchemy import DECIMAL
from yookassa import Payment, Configuration
import uuid

from config import YOOKASSA_ACCIUNT_ID, YOOKASSA_SECRET_KEY


Configuration.account_id = YOOKASSA_ACCIUNT_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


async def create_payment_request(amount: DECIMAL,
                                 chat_id: int) -> tuple[str, str | None]:
    """
    Создание заявки на оплату товаров из корзины.

    Args:
        amount: Сумма оплаты
        chat_id: ID пользователя

    Retuenrs:
        Возвращает ссылку на оплату товара (в ЮКАССЕ),
        а так же ID пользвоателя
    """
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "redirect_url": "https://t.me/ShopTraningBot"
        },
        "capture": True,
        "metadata": {
            "chat_id": chat_id
        },
        "description": "Описание товара..."
        }, id_key)
    return payment.confirmation.confirmation_url, payment.id
