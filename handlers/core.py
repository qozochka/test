from keyboards.core_keyboards import get_main_keyboard
from aiogram.types import Message


async def start(message: Message) -> None:
    """ Хендлер для команды /start """
    await message.answer("Добро пожаловать!", reply_markup=get_main_keyboard())