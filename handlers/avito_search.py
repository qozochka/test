""" Модуль реализующий поиск по квартирам Авито """

import json
from classes.flat import Flat
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from parser.controller import Controller
from avito_parser.Parser import Parser
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from data.queries import get_settings, save_current_avito_page, get_current_avito_page, get_current_array_page, \
    save_current_array_page

import time
from avito_parser.ConnectionJs import ConectionJs
from selenium.webdriver import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from avito_parser.avito_parsing import AvitoParsing

avito_search_router = Router()
options = Options()

options.add_argument("--headless")
driver = uc.Chrome(options=options)
actions = ActionChains(driver)

@avito_search_router.message(F.text == "Поиск")
async def search(message: Message) -> None:
    """Парсинг данных, выдача пользователю менюшки где можно листать квартиры"""
    connectionJs = ConectionJs()
    uid = message.from_user.id

    await message.answer("Парсинг данных с Авито...")

    # Корректно ли сораняются сеттингс в бд? в фром флэn и фром локэйшнс сохранение сеттингс в бд (вписал туда доп для авито)

    get_and_save_url(uid, 1)

    user_url = connectionJs.select_url_by_user_id(uid)[1]

    print("---" * 10)
    print(user_url)
    print(user_url)
    print(user_url)
    print(user_url)
    print(user_url)
    print("---" * 10)

    user = Parser(user_url, driver, actions, 1)

    save_current_avito_page(uid, 1)
    save_current_array_page(uid, 1)

    user.get_items()
    answer = "".join(user.format_data())

    await message.answer(f"{answer}", reply_markup=get_page_keyboard(), disable_web_page_preview=True)


@avito_search_router.callback_query(F.data == "next_page")
async def get_next_page(callback: CallbackQuery) -> None:
    """Перелистывает на следующую страницу"""
    uid = callback.from_user.id
    controller = Controller()
    user = Parser(controller.show_url_by_user_id(uid), driver, actions)
    await callback.message.answer("Парсинг данных c Авито...")

    flats = get_flats(uid, 5)
    answer = user.format_data(flats)
    await callback.message.answer(f"{answer}", reply_markup=get_page_keyboard(), disable_web_page_preview=True)
    await callback.answer()


def get_page_keyboard() -> InlineKeyboardMarkup:
    """ Создаёт инлайн клавиатуру для листания страниц """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Следующая страница",
        callback_data="next_page_avito"
    ))
    return builder.as_markup()


# def extract_correct_values(values: list[Flat], district) -> list[Flat]:
#     """ Возвращает подходящие по району квартиры """
#     result = []
#     for k in values:
#         if district == k.district:
#             result.append(k)
#     return result


# def get_flats(uid, result_amount: int, user: Parser) -> list[Flat]:
#     """ Получает result_amount квартир из парсера """
#     settings = json.loads(get_settings(uid))
#     district = None
#     try:
#         district = settings["district"]
#     except KeyError as err:
#         print(err)
#     flats = []
#     current_page = get_current_avito_page(uid)
#     array_page = get_current_array_page(uid)
#     while len(flats) < result_amount:
#         print("ARRAY_PAGE:")
#         print(array_page)
#         print("DATA:")
#         data = user.get_items() # тут2
#         print(data)
#         print("------")
#         first_five = data[(array_page - 1) * result_amount:array_page * result_amount]
#         print(first_five)
#         if district:
#             flats.extend(extract_correct_values(first_five, district))
#         else:
#              flats.extend(first_five)
#         if len(flats) > result_amount:
#             flats = flats[0:5]
#             array_page += 1
#             save_current_array_page(uid, array_page)
#             break
#         if array_page * 5 > len(data):
#             current_page += 1
#             save_current_avito_page(uid, current_page)
#             save_current_array_page(uid, 1)
#         else:
#             save_current_array_page(uid, array_page + 1)
#     return flats


def get_and_save_url(uid, page: int) -> list[Flat]:
    """ Получает settings из db и сохраняет ссылку в json  """
    controller = Controller()
    connectionJs = ConectionJs()
    settings = json.loads(get_settings(uid))

    city = district = min_price = rooms = without_deposit = without_commission = cost_max = ""
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

    try:
        without_deposit = settings["without_deposit"]
    except KeyError as err:
        print(err)

    try:
        without_commission = settings["without_commission"]
    except KeyError as err:
        print(err)

    try:
        cost_max = settings["cost_max"]
    except KeyError as err:
        print(err)

    filter_settings = {
        "start_page": page,
        "only_flat": True,
        "sort_by": "price_from_min_to_max",
        "min_price": min_price,
        "cost_max": cost_max,
        "without_commission": without_commission,
        "without_deposit": without_deposit,
    }
    print("NNNNNNN" * 10) # ok
    print([city, district], rooms, min_price, cost_max, without_commission, without_deposit, driver, actions)
    print("NNNNNNN" * 10)

    for_url = AvitoParsing([city, district], rooms, min_price, cost_max, without_commission, without_deposit, driver, actions)
    user_url = for_url.get_user_url() # Почему-то возвращает None

    print("***" * 10)
    print(user_url)
    print(user_url)
    print(user_url)
    print(user_url)
    print(user_url)
    print("***" * 10)


    connectionJs.insert_data(uid, user_url) # сохраняем url в json

    # values = []
    # if district:
    #     values = extract_correct_values(answer, district)
    # else:
    #     values = answer

    #return filter_settings