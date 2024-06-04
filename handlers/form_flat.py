""" Модуль с вводом параметров квартиры """

import json
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data.queries import save_settings
from keyboards.core_keyboards import get_main_keyboard
from utils.forms import FlatForm
from utils.utils import isInteger


flat_router = Router()

@flat_router.message(F.text.casefold() == "выбрать параметры квартиры")
async def select_rooms(message: Message, state: FSMContext) -> None:
    """ Начало заполнения данных о квартире """
    await message.answer("Заполните информацию о квартире. Для пропуска пишите -")
    await message.answer("Введите количество комнат (от 1 до 5)")
    await state.set_state(FlatForm.GET_ROOMS)



@flat_router.message(FlatForm.GET_ROOMS)
async def select_price(message: Message, state: FSMContext) -> None: 
    """ Начало заполнения данных о цене квартиры """
    if (message.text == "-"):
        await message.answer("Ввод количества комнат пропущен.")
    else:
        if not isInteger(message.text):
            await message.answer("Неверный ввод. Количество комнат должно быть целочисленным значением.")
            await message.answer("Введите количество комнат (от 1 до 5)")
            return
        
        if int(message.text) > 5 or int(message.text) < 1:
            await message.answer("Неверный ввод.")
            await message.answer("Введите количество комнат (от 1 до 5)")
            return
        
        input = int(message.text)
        
        await state.update_data(rooms = input)
        await message.answer(f"Вы выбрали количество комнат: {input}")

    await state.set_state(FlatForm.GET_PRICE)
    await message.answer("Введите минимальную цену квартиры:")


@flat_router.message(FlatForm.GET_PRICE)
async def form_flat_end(message: Message, state: FSMContext) -> None:
    """ Конец заполнения данных о квартире """
    if message.text == "-":
        await message.answer("Выбор цены пропущен.")
    else:
        if (not isInteger(message.text)):
            await message.answer("Неверный ввод. Цена должна быть целочисленными значением.")
            return
        minimum = int(message.text)
        if minimum > 100000000:
            await message.answer("Слишком большое значение")
            await message.answer("Введите минимальную цену квартиры")
            return
        if minimum < 1:
            await message.answer("Минимальная цена должна быть неотрицательным значением.")
            await message.answer("Введите минимальную цену квартиры")
            return
        await state.update_data(min_price = minimum)

    data = await state.get_data()
    save_settings(message.from_user.id, json.dumps(data))
    await message.answer("Информация о квартире заполнена.", reply_markup=get_main_keyboard())
    await state.set_state()

