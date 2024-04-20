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
                    text="Поиск"
                ),
            ]
        ], 
        resize_keyboard=True, 
        one_time_keyboard=True, 
        input_field_placeholder="Выбери действие", 
        selective=True
    )