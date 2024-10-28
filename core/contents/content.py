"""
Модуль с контентом для бота.

Args:
    user_menu: Кнопки пользователя
    admin_menu: Кнопки админа
    fsm_product: Добавление нового товара в БД
"""
user_menu = {
    1: "🚀КАТАЛОГ🚀",
    2: "🗑️КОРЗИНА🗑️",
    3: "🏧БАЛАНС🏧",
    4: "🗿РЕФЕРАЛЫ🗿",
    5: "📞КОНТАКТЫ📞",
    6: "💯В КОРЗИНУ💯",
    7: "💔УБРАТЬ ИЗ КОРЗИНЫ💔",
}

admin_menu = {
    1: "✅ДОБАВИТЬ ТОВАР✅",
    2: "❌УДАЛИТЬ❌",
    3: "🎫СГЕНЕРИРОВАТЬ ГИФТ🎫",
    4: "💲ПОПОЛНИТЬ БАЛАНС💲",
    5: "💸СПИСАТЬ СУММУ💸",
    6: "💫ВОЗВРАТ💫",
}

fsm_product = {
    1: "Введите название товара...",
    2: "Теперь введите описание товара...",
    3: "Укажите цену товара...",
    4: "Добавьте фото товара...",
    5: "Товар добавлен!",
    6: "Ошибка добавления товара!",
}
