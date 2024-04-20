""" Основной модуль. Запускает бота """

import asyncio
import os
import logging
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from handlers.core import start, show_settings
from handlers.form_flat import flat_router
from handlers.form_location import location_router
from data.queries import initialize_database
from utils.commands import set_commands
from middlewares.SaveUserMiddleware import SaveUserMiddleware

load_dotenv()
token = os.getenv('TOKEN')

async def main() -> None:
    """Запуск бота"""
    bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'))

    dp = Dispatcher()
    dp.message.middleware.register(SaveUserMiddleware())
    dp.include_routers(location_router, flat_router)

    dp.message.register(start, CommandStart())
    dp.message.register(show_settings, F.text == "Посмотреть настройки")

    await set_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    initialize_database()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())