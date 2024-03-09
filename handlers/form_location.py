""" Выбор расположения квартиры """

from utils.forms import SearchForm

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def form_location(message: Message, state: FSMContext):
    """ Начало заполнения данных о расположении квартиры """

    await message.answer("Введите город (или - чтобы пропустить)")
    await state.set_state(SearchForm.GET_CITY)


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
