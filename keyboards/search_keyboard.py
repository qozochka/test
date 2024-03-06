from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_search_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Выбрать город",
                    callback_data="choose_city",
                ),
                InlineKeyboardButton(
                    text="Выбрать район",
                    callback_data="choose_district",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Выбрать улицу",
                    callback_data="choose_street",
                ),
                InlineKeyboardButton(
                    text="Выбрать тип поиска",
                    callback_data="choose_search_type",
                ),
            ]
        ]
    )