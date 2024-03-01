from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType


async def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Основная клавиатура"""
    return ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
               text="Задать параметры поиска" 
            ),
        ],
        [
            KeyboardButton(
                text="Получать обновления"
            ),
            KeyboardButton(
                text="Не получать обновления"
            ),
        ]
    ], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие", selective=True)


async def start(message: Message) -> None:
    """Хендлер для команды /start"""
    print('here')
    kb = await get_main_keyboard()
    await message.answer("Добро пожаловать!", reply_markup=kb)