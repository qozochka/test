""" Выбор расположения квартиры """

import requests
from aiogram.client import bot

from utils.forms import SearchForm
from keyboards.core_keyboards import get_search_keyboard
from aiogram.types import Message
from aiogram.fsm.context import FSMContext





async def get_location_info(latitude, longitude):
    api_key = '1d8d9808-b416-418d-8215-e8b0b6c6f3d9'
    url = f'https://catalog.api.2gis.ru/3.0/items/geocode?type=street%2Cbuilding%2Cattraction%2Cstation_platform%2Cadm_div.place%2Cadm_div.city%2Cadm_div.district&key={api_key}&fields=items.point%2Citems.region_id%2Citems.segment_id&location=37.64%2C55.74' \


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


async def handle_location(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    # Получаем информацию о городе и районе из API 2ГИС
    city, district = await get_location_info(latitude, longitude)



    # После получения информации сохраняем ее в состоянии
    await state.update_data(city=city, district=district)
    # Отправляем сообщение пользователю с информацией о городе и районе
    if city and district:
        await message.answer(f"Вы находитесь в городе {city}, район {district}")
    else:
        await message.answer("Извините, не удалось определить ваше местоположение.")



async def form_location(message: Message, state: FSMContext):
    """ Начало заполнения данных о расположении квартиры """

    await message.answer("сигма", reply_markup=await get_search_keyboard())

    await state.set_state(SearchForm.GET_LOCATIONS)



async def select_district(message: Message, state: FSMContext):
    """ Запускается после того как пользователь выбрал город, требует выбрать район """

    answer = "Выбор города пропущен."
    if message.text != "-":
        answer = f"Вы выбрали город: {message.text}."
        await state.update_data(city=message.text)
    answer += "\nТеперь выберите район (или - чтобы пропустить)"
    
    await message.answer(answer)
    await state.set_state(SearchForm.GET_DISTRICT)


async def select_street(message: Message, state: FSMContext):
    """ Запускатеся после того как пользователь выбрал район, требует выбрать улицу """

    answer = "Выбор района пропущен."
    if message.text != "-":
        answer = f"Вы выбрали район: {message.text}."
        await state.update_data(district=message.text)
    answer += "\nТеперь выберите улицу (или - чтобы пропустить)"

    await message.answer(answer)
    await state.set_state(SearchForm.GET_STREET)


async def form_location_end(message: Message, state: FSMContext):
    """ Конец заполнения данных о квартире """

    answer = "Выбор улицы пропущен."
    if message.text != "-":
        answer = f"Вы выбрали улицу: {message.text}."
        await state.update_data(street=message.text)
    
    await message.answer(answer)
    await state.set_state()
