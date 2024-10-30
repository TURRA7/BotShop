import random
import string


async def generate_code(length: int = 8) -> str:
    """
    Генерирует строку(код из случайных букв и цифр).

    Args:

        length: Количество символов в строке

    Returns:

        Возвращает сгенерированную строку,
        с случайными символами
    """
    characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
                  "ghijklmnopqrstuvwxyz0123456789")
    return ''.join(random.choices(characters, k=length))


async def generate_gift() -> str:
    """
    Генерирует строку формата XXXX-XXXX-XXXX-XXXX.

    Returns:

        Возвращает сгенерированную строку,
        с случайными символами
    """
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    code = ''.join(random.choice(characters) for _ in range(16))
    formatted_code = '-'.join(code[i:i+4] for i in range(0, 16, 4))
    return formatted_code