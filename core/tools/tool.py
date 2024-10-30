import random


async def generate_gift(length: int = 8) -> str:
    """
    Генерирует строку(код из случайных букв и цифр).

    Args:

        length: Количество символов в строке

    Returns:

        Возвращает сгенерированную строку,
        с случацными символами
    """
    characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
                  "ghijklmnopqrstuvwxyz0123456789")
    return ''.join(random.choices(characters, k=length))
