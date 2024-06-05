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
    """  Заполнение данных о квартире """
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
        if minimum < 0:
            await message.answer("Минимальная цена должна быть неотрицательным значением.")
            await message.answer("Введите минимальную цену квартиры")
            return
        await state.update_data(min_price = minimum)

    await state.set_state(FlatForm.GET_COST_MAX)
    await message.answer("Введите максимальную цену квартиры (только для Авито):")


@flat_router.message(FlatForm.GET_COST_MAX)
async def form_flat_end(message: Message, state: FSMContext) -> None:
    """ Заполнение данных о квартире """
    if message.text == "-":
        await message.answer("Выбор цены пропущен.")
    else:
        if (not isInteger(message.text)):
            await message.answer("Неверный ввод. Цена должна быть целочисленными значением.")
            return
        cost_max_here = int(message.text)
        if cost_max_here > 100000000:
            await message.answer("Слишком большое значение")
            await message.answer("Введите максимальнуя цену квартиры")
            return
        if cost_max_here < 0:
            await message.answer("Максимальная цена должна быть неотрицательным значением.")
            await message.answer("Введите максимальную цену квартиры")
            return
        await state.update_data(cost_max = cost_max_here)

    await state.set_state(FlatForm.GET_WITHOUT_COMMISION)
    await message.answer("Без комиссии да/нет (только для Авито):")

@flat_router.message(FlatForm.GET_WITHOUT_COMMISION)
async def form_flat_end(message: Message, state: FSMContext) -> None:
    """ Заполнение данных о квартире """

    commision_flag = (message.text).lower()

    if not(commision_flag in ("да","нет",)):
        await message.answer("Нет такого варианта")
        await message.answer("Введите корректное значение (да/нет)")
        return
    
    if commision_flag == 'да':
        commision_flag = True
    elif commision_flag == 'нет':
        commision_flag = False
    else:
        return

    await state.update_data(without_commission = commision_flag)

    await state.set_state(FlatForm.GET_WITHOUT_DEPOSIT)
    await message.answer("Без депозита да/нет (только для Авито):")

@flat_router.message(FlatForm.GET_WITHOUT_DEPOSIT)
async def form_flat_end(message: Message, state: FSMContext) -> None:
    """ Последнее заполнение данных о квартире """

    deposit_flag = (message.text).lower()
    if not(deposit_flag in ("да","нет",)):
        await message.answer("Нет такого варианта")
        await message.answer("Введите корректное значение (да/нет)")
        return
    
    if deposit_flag == 'да':
        deposit_flag = True
    elif deposit_flag == 'нет':
        deposit_flag = False
    else:
        return

    await state.update_data(without_deposit = deposit_flag)

    data = await state.get_data()
    save_settings(message.from_user.id, json.dumps(data))
    await message.answer("Информация о квартире заполнена.")
    await state.set_state()
    
