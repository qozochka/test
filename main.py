import asyncio
import os
import logging
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties

load_dotenv()
token = os.getenv('TOKEN')

dp = Dispatcher()

async def main() -> None:
    """Запуск бота"""
    bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())