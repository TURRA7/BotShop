"""
Модуль конфигурации приложения.

Func:

    load_dotenv: Парсит данные из окружения

Args:

    TOKEN: Токен бота, полученый у @BotFather
    ADMIN_ID: ID администратора, полученое у @getmyid_bot
    PG_USER: Логин базы данных
    PG_PASS: Пароль базы данных
    PG_HOST: Хост базы данных
    PG_NAME: Название базы данных
"""
import os
from dotenv import load_dotenv


load_dotenv()

# Основные параметры
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

# Параметры подключения БД - PostgreSQL
PG_USER = os.environ.get("PG_USER")
PG_PASS = os.environ.get("PG_PASS")
PG_HOST = os.environ.get("PG_HOST")
PG_NAME = os.environ.get("PG_NAME")
