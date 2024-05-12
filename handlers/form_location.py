""" Модуль с вводом расположения квартиры """

import requests

from keyboards.core_keyboards import get_search_keyboard, get_main_keyboard
import json

from aiogram import F, Router

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data.queries import save_settings
from utils.forms import LocationForm
location_router = Router()

async def form_location(message: Message, state: FSMContext):
    """ Корявая хуета """

    await message.answer("сигма", reply_markup=get_search_keyboard()) # Это нужно исправить, я имею в виду сигму, но я не знаю как, соре:(

    await state.set_state(LocationForm.GET_LOCATIONS)
@location_router.message(LocationForm.GET_LOCATIONS)
async def handle_location(message: Message, state: FSMContext):
    if message.text == "выбрать рядом со мной":
        await state.set_state(LocationForm.NEAR_ME)
    elif message.text == "Ввести город вручную":
        await state.set_state(LocationForm.GET_CITY)

    else:
        await message.answer("Неверный выбор. Пожалуйста, выберите один из предложенных вариантов.")





async def get_location_info(latitude, longitude):
    api_key = '1d8d9808-b416-418d-8215-e8b0b6c6f3d9'
    url = f'https://catalog.api.2gis.ru/3.0/items/geocode?type=street%2Cbuilding%2Cattraction%2Cstation_platform%2Cadm_div.place%2Cadm_div.city%2Cadm_div.district&key={api_key}&fields=items.point%2Citems.region_id%2Citems.segment_id&location=37.64%2C55.74'
    params = {
        'q': f'{latitude},{longitude}',
        'key': api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'result' in data and data['result']:

            result = data['result']['items'][0]
            res = result["full_name"].split(', ')
            city = res[0]
            district = res[1]

            return city, district
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching location info: {e}")
        return None, None


location_router = Router()




@location_router.message(LocationForm.NEAR_ME)
async def handle_location(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    city, district = await get_location_info(latitude, longitude)

    await state.update_data(city=city, district=district)
    if city and district:
        await message.answer(f"Вы находитесь в городе {city}, район {district}")
        await message.answer("Ваши данные сохранены", reply_markup=get_main_keyboard())
        data = await state.get_data()
        save_settings(message.from_user.id, json.dumps(data))
        await message.answer("Информация о местоположении квартиры заполнена.")
        await state.set_state()
    else:
        await message.answer("Извините, не удалось определить ваше местоположение.",reply_markup=get_main_keyboard())






@location_router.message(LocationForm.GET_CITY)
async def select_district(message: Message, state: FSMContext) -> None:
    """ Запускается после того как пользователь выбрал город, требует выбрать район """
    if (message.text == "-"):
        await message.answer("Ввод города пропущен.")
    else:
        await message.answer(f"Вы выбрали город: {message.text}.")
        await state.update_data(city=message.text)

    await message.answer(f"\nТеперь введите район")
    await state.set_state(LocationForm.GET_DISTRICT)


@location_router.message(LocationForm.GET_DISTRICT)
async def select_street(message: Message, state: FSMContext) -> None:
    """ Запускатеся после того как пользователь выбрал район, требует выбрать улицу """
    if message.text == "-":
        await message.answer("Ввод района пропущен.")
    else:
        await message.answer(f"Вы выбрали район: {message.text}.")
        await state.update_data(district=message.text)

    await message.answer("\nТеперь выберите улицу")
    await state.set_state(LocationForm.GET_STREET)


@location_router.message(LocationForm.GET_STREET)
async def form_location_end(message: Message, state: FSMContext) -> None:
    """ Конец заполнения данных о расположении квартиры """
    if message.text == "-":
        await message.answer("Ввод улицы пропущен.")
    else:
        await message.answer(f"Вы выбрали улицу: {message.text}.")
        await state.update_data(street=message.text)

    data = await state.get_data()
    save_settings(message.from_user.id, json.dumps(data))

    await message.answer("Информация о местоположении квартиры заполнена.", reply_markup=get_main_keyboard())
    await state.set_state()
