from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



async def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Основная клавиатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
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
        ], 
        resize_keyboard=True, 
        one_time_keyboard=True, 
        input_field_placeholder="Выбери действие", 
        selective=True
    )