""" Модуль состояния форм """

from aiogram.fsm.state import StatesGroup, State


class LocationForm(StatesGroup):
    GET_CITY = State()
    GET_DISTRICT = State()
    GET_STREET = State()


class FlatForm(StatesGroup):
    GET_ROOMS = State()
    GET_PRICE = State()
    GET_FLOOR = State()
