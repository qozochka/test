from keyboards.main_keyboard import get_main_keyboard

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType


async def start(message: Message) -> None:
    """Хендлер для команды /start"""
    kb = await get_main_keyboard()
    await message.answer("Добро пожаловать!", reply_markup=kb)