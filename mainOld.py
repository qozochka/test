""" Основной модуль. Запускает бота """

import asyncio
import os
import logging
import sys
from utils.forms import LocationForm
from handlers.form_location import select_district, handle_location, form_end, form_location, \
    get_near_me
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from handlers.cian_search import cian_search_router
from handlers.avito_search import avito_search_router
from handlers.core import core_router
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
    dp.include_routers(location_router, flat_router, core_router, avito_search_router) # временно убрал Циан роутер

    await set_commands(bot)
    dp.message.register(form_location, F.text == "Выбрать местоположение квартиры")
    dp.message.register(handle_location, LocationForm.GET_LOCATIONS)
    dp.message.register(get_near_me, LocationForm.NEAR_ME)
    dp.message.register(select_district, LocationForm.GET_CITY)
    dp.message.register(form_end, LocationForm.GET_DISTRICT)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    initialize_database()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
