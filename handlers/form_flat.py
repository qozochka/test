""" Выбор параметров квартиры """

from utils.forms import SearchForm

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def form_flat(message: Message, state: FSMContext):
    """ Начало заполнения данных о расположении квартиры """

    await message.answer("Введите количество комнат (от 1 до 4, 5 для выбора \"5 или больше\", - чтобы пропустить.)")
    await state.set_state(SearchForm.GET_ROOMS)

