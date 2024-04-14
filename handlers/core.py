from keyboards.core_keyboards import get_main_keyboard, get_search_keyboard, get_type_keyboard

from aiogram.types import Message


async def start(message: Message) -> None:
    """ Хендлер для команды /start """
    kb = await get_main_keyboard()
    await message.answer("Добро пожаловать в бот-риелтор. Этот бот поможет вам с поиском недвижимости.", reply_markup=kb)