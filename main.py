import asyncio
import os
import logging
import sys

from aiogram.client import bot


from utils.commands import set_commands
from utils.forms import SearchForm
from handlers.core import start
from handlers.form_location import form_location, select_district, select_street, form_location_end, handle_location

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

    dp.message.register(start, CommandStart())
    dp.message.register(form_location, F.text == "Выбрать местоположение квартиры")
    dp.message.register(handle_location, SearchForm.GET_LOCATIONS)

    dp.message.register(select_district, SearchForm.GET_CITY)
    dp.message.register(select_street, SearchForm.GET_DISTRICT)
    dp.message.register(form_location_end, SearchForm.GET_STREET)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())