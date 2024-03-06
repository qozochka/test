from keyboards.search_keyboard import get_search_keyboard

from aiogram.types import Message


async def set_search_params(message: Message):
    kb = await get_search_keyboard()
    await message.answer("Выберите действие", reply_markup=kb)