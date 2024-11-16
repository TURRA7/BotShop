from yookassa import Payment, Configuration
import uuid

import yookassa

from config import YOOKASSA_ACCIUNT_ID, YOOKASSA_SECRET_KEY


Configuration.account_id = YOOKASSA_ACCIUNT_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


async def create_payment(amount: float,
                         chat_id: int,
                         description: str) -> tuple[str, str]:
    """
    Создание платежа в yookassa.

    Args:
        amount: Сумма
        chat_id: ID пользователя
        deescription: Описание/детали платежа

    Returns:
        Создаёт платёж в системе yookassa, возвращает
        ссылку на транзакцию и ID платежа.
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
            "return_url": "http://t.me/test_pay_apiBot"
        },
        "capture": True,
        "metadata": {
            "chat_id": chat_id
        },
        "description": description
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id


async def check_payment(payment_id: int) -> dict | bool:
    """
    Проверка платежа в yookassa.

    Args:
        payment_id: ID платежа в системе yookassa

    Returns:
        Проверяет статус платежа в системе yookassa,
        возвращает метадату платежа если статус 'succeeded',
        иначе False
    """
    payment = yookassa.Payment.find_one(payment_id=payment_id)
    if payment.status == 'succeeded':
        return payment.metadata
    else:
        return False


async def get_amount_payment(payment_id: int) -> float:
    """
    Получение суммы из платежа yookassa.

    Args:
        payment_id: ID платежа в системе yookassa

    Returns:
        Проверяет сумму из платежа yookassa.
    """
    payment = yookassa.Payment.find_one(payment_id=payment_id)
    return payment.amount.value
