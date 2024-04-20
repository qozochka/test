""" Модуль с основными командами бота """

import json
from aiogram.types import Message
from keyboards.core_keyboards import get_main_keyboard
from data.queries import get_settings


async def start(message: Message) -> None:
    """ Хендлер для команды /start """
    await message.answer("Добро пожаловать!", reply_markup=get_main_keyboard())


async def show_settings(message: Message) -> None:
    """ Хендлер для просмотра настроек """
    userid = message.from_user.id

    settings = get_settings(userid)
    if settings:
        settings = json.loads(settings)

    answer = location_settings_to_string(settings) + "\n\n" + flat_settings_to_string(settings)
    await message.answer(answer)


def location_settings_to_string(settings: dict) -> str:
    """ Приводит данные о местоположении квартиры в читабельный вид """
    if not settings:
        return "Местоположение квартиры:\nЛюбое"

    res = "Местоположение квартиры: "
    res += "\nГород: "
    res = concat_param(res, settings, "city")
    res += "\nРайон: "
    res = concat_param(res, settings, "district")
    res += "\nУлица: "
    res = concat_param(res, settings, "street")

    return res


def flat_settings_to_string(settings):
    """ Приводит данные о квартире в читабельный вид """
    if not (settings):
        return "Параметры квартиры:\nЛюбые"
    
    res = "Параметры квартиры: "
    res += "\nКоличество комнат: "
    res = concat_param(res, settings, "rooms")
    res += "\nЦеновой диапазон: "
    res = concat_price_range(res, settings)

    return res


def concat_param(string: str, settings: dict, key: str) -> str:
    """ Присоединяет параметр к строке, если он есть """
    try:
        string += f"{settings[key]}"
    except:
        string += "[Не заполнено]"

    return string


def concat_price_range(string: str, settings: dict) -> str:
    """ Присоединяет ценовой диапазон к строке (частный случай concat_param) """
    try:
        string += f"от {settings["priceRange"][0]} до {settings["priceRange"][1]}"
    except:
        string += "[Не заполнено]"

    return string