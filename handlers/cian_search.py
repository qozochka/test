""" Модуль реализующий поиск по квартирам циана """

import json
from classes.flat import Flat
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from parser.controller import Controller
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from data.queries import get_settings, save_current_cian_page, get_current_cian_page, get_current_array_page, save_current_array_page

cian_search_router = Router()

@cian_search_router.message(F.text == "Поиск")
async def search(message: Message) -> None:
    """Парсинг данных, выдача пользователю менюшки где можно листать квартиры"""
    uid = message.from_user.id
    await message.answer("Парсинг данных...")

    save_current_cian_page(uid, 1)
    save_current_array_page(uid, 1)

    flats = get_flats(uid, 5)
    answer = flats_to_string(flats)
    await message.answer(f"{answer}", reply_markup=get_page_keyboard(), disable_web_page_preview=True)


@cian_search_router.callback_query(F.data == "next_page")
async def get_next_page(callback: CallbackQuery) -> None:
    """Перелистывает на следующую страницу"""
    uid = callback.from_user.id
    await callback.message.answer("Парсинг данных...")

    flats = get_flats(uid, 5)
    answer = flats_to_string(flats)
    await callback.message.answer(f"{answer}", reply_markup=get_page_keyboard(), disable_web_page_preview=True)
    await callback.answer()


def get_page_keyboard() -> InlineKeyboardMarkup:
    """ Создаёт инлайн клавиатуру для листания страниц """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Следующая страница",
        callback_data="next_page"
    ))
    return builder.as_markup()


def extract_correct_values(values: list[Flat], district) -> list[Flat]:
    """ Возвращает подходящие по району квартиры """
    result = []
    for k in values:
        if district == k.district:
            result.append(k)
    return result


def flats_to_string(flats: list[Flat]) -> str:
    """ Преобразует список квартир в читабельный вид """
    text = ""
    for flat in flats:
        text += str(flat) + "\n\n"
    return text


def get_flats(uid, result_amount: int) -> list[Flat]:
    """ Получает result_amount квартир из парсера """
    settings = json.loads(get_settings(uid))
    district = None
    try:
        district = settings["district"]
    except KeyError as err:
        print(err)
    flats = []
    current_page = get_current_cian_page(uid)
    array_page = get_current_array_page(uid)
    while len(flats) < result_amount:
        print("ARRAY_PAGE:")
        print(array_page)
        print("DATA:")
        data = get_data(uid, current_page)
        print(data)
        print("------")
        first_five = data[(array_page - 1) * result_amount:array_page * result_amount]
        print(first_five)
        if district:
            flats.extend(extract_correct_values(first_five, district))
        else:
             flats.extend(first_five)
        if len(flats) > result_amount:
            flats = flats[0:5]
            array_page += 1
            save_current_array_page(uid, array_page)
            break
        if array_page * 5 > len(data):
            current_page += 1
            save_current_cian_page(uid, current_page)
            save_current_array_page(uid, 1)
        else:
            save_current_array_page(uid, array_page + 1)
    return flats


def get_data(uid, page: int) -> list[Flat]:
    """ Возвращает список квартир (Flat) со страницы page """
    settings = json.loads(get_settings(uid))
    controller = Controller()
    city = district = min_price = rooms = ""
    try:
        city = settings["city"]
    except KeyError as err:
        print(err)
    try:
        rooms = settings["rooms"]
    except KeyError as err:
        rooms = 1
        print(err)
    try:
        district = settings["district"]
    except KeyError as err:
        print(err)
    try:
        min_price = settings["min_price"]
    except KeyError as err:
        min_price = 0
        print(err)
    filter_settings = {
        "start_page": page,
        "only_flat": True,
        "sort_by": "price_from_min_to_max",
        "min_price": min_price,
    }

    controller.add_user_url(uid, controller.parsing_url(rooms, location=f"{city}", **filter_settings))
    answer = controller.parsing_from_url(uid)

    values = []
    if district:
        values = extract_correct_values(answer, district)
    else:
        values = answer

    return values