""" Модуль состояния форм """

from aiogram.fsm.state import StatesGroup, State


class LocationForm(StatesGroup):
    NEAR_ME = State()
    GET_CITY = State()
    GET_DISTRICT = State()
    GET_STREET = State()
    GET_LOCATIONS = State()
    GET_USER_LOCATIONS = State()


class FlatForm(StatesGroup):
    GET_ROOMS = State()
    GET_FLOOR = State()
    GET_PRICE = State()
    GET_PRICE = State()
    GET_COST_MAX = State()
    GET_WITHOUT_COMMISION = State()
    GET_WITHOUT_DEPOSIT = State()

