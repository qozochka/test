import asyncio
from handlers.cian_search import extract_correct_values, get_data
import os
import logging
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from handlers.cian_search import cian_search_router
from handlers.core import core_router
from handlers.form_flat import flat_router
from handlers.form_location import location_router
from data.queries import initialize_database
from utils.commands import set_commands
from middlewares.SaveUserMiddleware import SaveUserMiddleware
import json
from classes.flat import Flat
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from parser.controller import Controller
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from data.queries import get_settings, get_newest_cian_id, save_newest_cian_id, get_ids



async def cian_search_update(bot: Bot):
    while True:
        try:
            ids = get_ids()
            for uid in ids:
                flat = await get_new_flat(uid)
                if flat:
                    await bot.send_message(uid, "Найдена новая квартира по вашему запросу: " + flat.link)
                    print("MESSAGE_SENT")
        except:
            print("UPDATE FAILED.")
        print("loop iteration.")
        await asyncio.sleep(120)  # Подождать 120 секунд перед следующей итерацией


async def get_new_flat(uid) -> Flat:
    """ Получает result_amount квартир из парсера """
    settings = json.loads(get_settings(uid))
    district = None
    try:
        district = settings["district"]
    except KeyError as err:
        print(err)
    flats = []
    current_page = 1
    while len(flats) < 1:
        data = get_data(uid, current_page, "creation_data_from_newer_to_older")
        if len(data) == 0:
            return []
        if district:
            flats.extend(extract_correct_values(data, district))
        else:
            flats.extend(data)
        if current_page == 3:
            return None
        current_page += 1
    
    try:
        link_id = int(extract_id_from_link(flats[0].link))
        newest_id = int(get_newest_cian_id(uid))
        if int(link_id) == int(newest_id):
            return None
    except:
        pass
    save_newest_cian_id(uid, link_id)
    return flats[0]



def extract_id_from_link(link: str) -> int:
    idx = link.index("flat/")
    link = link[idx + 5:]
    link = link[:-1]
    return link

