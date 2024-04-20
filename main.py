import asyncio
import os
import logging
import sys

from utils.commands import set_commands
from handlers.core import start
from handlers.form_flat import flat_router
from handlers.form_location import location_router

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

load_dotenv()
token = os.getenv('TOKEN')

async def main() -> None:
    """Запуск бота"""

    bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(location_router, flat_router)
    await set_commands(bot)
    dp.message.register(start, CommandStart())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())