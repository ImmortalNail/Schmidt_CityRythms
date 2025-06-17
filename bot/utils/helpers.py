import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import dp  # импортируем готовый Dispatcher с хэндлерами
from admin import dp as admin_dp  # админский dp для регистрации админ-хэндлеров
from database import init_db

logging.basicConfig(level=logging.INFO)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Ошибка: BOT_TOKEN не найден в .env")

bot = Bot(token=BOT_TOKEN)
dp.bot = bot
dp.storage = None  # если хочешь, можно подключить MemoryStorage, Redis и т.п.

# Регистрируем админские хэндлеры тоже
dp.include_router(admin_dp)  # в aiogram 2.x можно просто регистрировать функции — этот момент потом адаптируем

async def main():
    logging.info("Инициализация базы данных...")
    await init_db()

    logging.info("Запуск polling...")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())