""" Выбор расположения квартиры """

from utils.forms import LocationForm

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


location_router = Router()

@location_router.message(F.text.casefold() == "выбрать местоположение квартиры")
async def select_city(message: Message, state: FSMContext) -> None:
    """ Требует выбрать город """

    await message.answer("Заполните информацию о расположении квартиры. Для пропуска пишите -")
    await message.answer("Введите город")
    await state.set_state(LocationForm.GET_CITY)


@location_router.message(LocationForm.GET_CITY)
async def select_district(message: Message, state: FSMContext) -> None:
    """ Запускается после того как пользователь выбрал город, требует выбрать район """

    if (message.text == "-"):
        await message.answer("Ввод города пропущен.")
    else:
        await message.answer(f"Вы выбрали город: {message.text}.")
        await state.update_data(city = message.text)

    await message.answer(f"\nТеперь введите район")
    await state.set_state(LocationForm.GET_DISTRICT)


@location_router.message(LocationForm.GET_DISTRICT)
async def select_street(message: Message, state: FSMContext) -> None:
    """ Запускатеся после того как пользователь выбрал район, требует выбрать улицу """

    if message.text == "-":
        await message.answer("Ввод района пропущен.")
    else:
        await message.answer(f"Вы выбрали район: {message.text}.")
        await state.update_data(district = message.text)

    await message.answer("\nТеперь выберите улицу")
    await state.set_state(LocationForm.GET_STREET)


@location_router.message(LocationForm.GET_STREET)
async def form_location_end(message: Message, state: FSMContext) -> None:
    """ Конец заполнения данных о расположении квартиры """

    if message.text == "-":
        await message.answer("Ввод улицы пропущен.")
    else: 
        await message.answer(f"Вы выбрали улицу: {message.text}.")
        await state.update_data(street = message.text)
    
    await message.answer("Информация о местоположении квартиры заполнена.")
    await state.set_state()