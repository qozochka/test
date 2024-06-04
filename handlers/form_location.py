""" Модуль с вводом расположения квартиры """
import time

import aiohttp

from keyboards.core_keyboards import get_search_keyboard, get_main_keyboard
import json

from aiogram import F, Router

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data.queries import save_settings
from utils.forms import LocationForm

location_router = Router()


@location_router.message(F.text.casefold() == "выбрать местоположение квартиры")
async def form_location(message: Message, state: FSMContext) -> None:
    await state.set_state(LocationForm.GET_LOCATIONS)
    print("Установлено состояние GET_LOCATIONS")

    await message.answer("Ожидание выбора местоположения...", reply_markup=get_search_keyboard())



@location_router.message(LocationForm.GET_LOCATIONS)
async def handle_location(message: Message, state: FSMContext):
    if message.location:
        print(message.location)
        await state.set_state(LocationForm.NEAR_ME)
        await process_near_me(message,state)

        print("Переход в состояние near me")
    elif message.text == "Ввести город вручную":
        await message.answer("Заполните информацию о расположении квартиры. Для пропуска пишите -")
        await message.answer("Введите город")
        await state.set_state(LocationForm.GET_CITY)

    else:
        await message.answer("Неверный выбор. Пожалуйста, выберите один из предложенных вариантов.")


async def get_location_info(latitude, longitude):
    api_key = '28612374-30e3-42fd-bdb2-2a874f316862'
    url = f"https://catalog.api.2gis.com/3.0/items/geocode"
    print("Пытаюсь получить данные из апишки")
    params = {
        'lat': latitude,
        'lon': longitude,
        'fields': 'items.point,items.full_name',
        'key': api_key
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()

                if 'result' in data and data['result']:
                    result = data['result']['items'][0]
                    res = result["full_name"].split(', ')
                    city = res[0]
                    district = res[1]
                    print(city, district)
                    return city, district

                else:
                    print('Ne polychilos')
                    return None, None
    except Exception as e:
        print(f"Error fetching location info: {e}")
        return None, None

async def process_near_me(message: Message, state: FSMContext):
    print("Пытаюсь обработать состояние NEAR_ME")
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    city, district = await get_location_info(latitude, longitude)
    await state.update_data(city=city, district=district)
    if city and district:
        await message.answer(f"Вы находитесь в городе {city}, район {district}", reply_markup=get_main_keyboard())
        data = await state.get_data()
        save_settings(message.from_user.id, json.dumps(data))
        await message.answer("Информация о местоположении квартиры заполнена.")
        await state.clear()
    else:
        await message.answer("Извините, не удалось определить ваше местоположение.", reply_markup=get_main_keyboard())

@location_router.message(LocationForm.NEAR_ME)
async def get_near_me(message: Message, state: FSMContext):
    await process_near_me(message, state)

@location_router.message(LocationForm.GET_CITY)
async def select_district(message: Message, state: FSMContext) -> None:
    """ Запускается после того как пользователь выбрал город, требует выбрать район """
    if message.text == "-":
        await message.answer("Ввод города пропущен.")
    else:
        await message.answer(f"Вы выбрали город: {message.text}.")
        await state.update_data(city=message.text)

    await message.answer(f"\nТеперь введите район")
    await state.set_state(LocationForm.GET_DISTRICT)


@location_router.message(LocationForm.GET_DISTRICT)
async def form_end(message: Message, state: FSMContext) -> None:
    """ Запускается после того как пользователь выбрал район """
    if message.text == "-":
        await message.answer("Ввод района пропущен.")
    else:
        await message.answer(f"Вы выбрали район: {message.text}.")
        await state.update_data(district=message.text)
    data = await state.get_data()
    save_settings(message.from_user.id, json.dumps(data))
    await message.answer("Информация о местоположении квартиры заполнена.", reply_markup=get_main_keyboard())
    await state.set_state()
