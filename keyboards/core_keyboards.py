""" Модуль основных клавиатур """

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
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
                    text="Посмотреть параметры квартиры"
                ),
                KeyboardButton(
                    text="Поиск по Циану"
                ),
                KeyboardButton(
                    text="Поиск по Авито"
                ),
            ]
        ], 
        resize_keyboard=True, 
        one_time_keyboard=True, 
        input_field_placeholder="Выбери действие", 
        selective=True
    )


def get_search_keyboard() -> ReplyKeyboardMarkup:
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
                    text="Ввести город вручную"
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери действие",
        selective=True
    )


