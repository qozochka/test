from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



async def get_main_keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура основного действия """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Выбрать местоположение квартиры" 
                ),
                KeyboardButton(
                    text="Выбрать параметры квартиры"
                ),
            ],
            [
                KeyboardButton(
                    text="Поиск"
                ),
            ]
        ], 
        resize_keyboard=True, 
        one_time_keyboard=True, 
        input_field_placeholder="Выбери действие", 
        selective=True
    )


async def get_search_keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура отвечающая за выбор места квартиры """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Выбрать рядом со мной",
                    request_location=True

                ),
            ],
            [
                KeyboardButton(
                    text="Выбрать город из списка:"
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери действие",
        selective=True

    )


async def get_type_keyboard() -> InlineKeyboardMarkup:
    """ Клавиатура отвечающая за выбор типа квартиры """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Количество комнат",
                    callback_data="flat_rooms",
                ),
                InlineKeyboardButton(
                    text="Цена",
                    callback_data="flat_price",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Этаж",
                    callback_data="flat_floor",
                ),
                InlineKeyboardButton(
                    text="Арендодатель",
                    callback_data="flat_landlord",
                )
            ]
        ]
    )