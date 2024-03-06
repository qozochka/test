import asyncio
import os
import logging
import sys

from utils.commands import set_commands
from handlers import start, search_params

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import BotCommand
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties

load_dotenv()
token = os.getenv('TOKEN')

dp = Dispatcher()

async def main() -> None:
    """Запуск бота"""

    bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'))
    await set_commands(bot)

    dp.message.register(start.start, CommandStart())
    dp.message.register(search_params.set_search_params, F.text == "Задать параметры поиска")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())