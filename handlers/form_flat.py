""" Модуль с вводом параметров квартиры """

import json
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data.queries import save_settings
from utils.forms import FlatForm
from utils.utils import isInteger


flat_router = Router()

@flat_router.message(F.text.casefold() == "выбрать параметры квартиры")
async def select_rooms(message: Message, state: FSMContext) -> None:
    """ Начало заполнения данных о квартире """
    await message.answer("Заполните информацию о квартире. Для пропуска пишите -")
    await message.answer("Введите количество комнат")
    await state.set_state(FlatForm.GET_ROOMS)



@flat_router.message(FlatForm.GET_ROOMS)
async def select_price(message: Message, state: FSMContext) -> None: 
    """ Начало заполнения данных о цене квартиры """
    if (message.text == "-"):
        await message.answer("Ввод количества комнат пропущен.")
    else:
        if not isInteger(message.text):
            await message.answer("Неверный ввод. Количество комнат должно быть целочисленным значением.")
            await message.answer("Введите количество комнат (от 1 до 4, 5 для выбора \"5 или больше\"")
            return
        
        input = int(message.text)
        
        if (input > 5):
            await state.update_data(rooms = 5)
            await message.answer(f"Вы выбрали количество комнат: 5 или больше")
        else:
            await state.update_data(rooms = input)
            await message.answer(f"Вы выбрали количество комнат: {input}")

    await message.answer("Введите минимальную и максимальную цену квартиры через пробел (например: 0 10000000)")
    await state.set_state(FlatForm.GET_PRICE)


@flat_router.message(FlatForm.GET_PRICE)
async def form_flat_end(message: Message, state: FSMContext) -> None:
    """ Конец заполнения данных о квартире """
    if message.text == "-":
        await message.answer("Выбор цены пропущен.")
    else:
        range = message.text.split(' ');
        if (len(range) != 2):
            await message.answer("Неверный ввод.")
            await message.answer("Введите минимальную и максимальную цену квартиры через пробел (например: 0 10000000)")
            return
        
        if (not isInteger(range[0])) or (not isInteger(range[1])):
            await message.answer("Неверный ввод. Минимум и максимум должны быть целочисленными значениями.")
            await message.answer("Введите минимальную и максимальную цену квартиры через пробел (например: 0 10000000)")
            return
        
        minimum = int(range[0])
        maximum = int(range[1])
        
        if (maximum < 0) or (minimum < 0):
            await message.answer("Неверный ввод. Максимум и минимум цены должны быть неотрицательными числами")
            await message.answer("Введите минимальную и максимальную цену квартиры через пробел (например: 0 10000000)")
            return

        if (maximum <= minimum):
            await message.answer("Неверный ввод. Максимум цены должен быть выше минимума.")
            await message.answer("Введите минимальную и максимальную цену квартиры через пробел (например: 0 10000000)")
            return
        await state.update_data(priceRange = [minimum, maximum])

    data = await state.get_data()
    save_settings(message.from_user.id, json.dumps(data))
    await message.answer("Информация о квартире заполнена.")
    await state.set_state()

