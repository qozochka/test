from aiogram.fsm.state import StatesGroup, State


class SearchForm(StatesGroup):
    GET_CITY = State()
    GET_DISTRICT = State()
    GET_STREET = State()
    GET_ROOMS = State()
    GET_FLOOR = State()
    GET_LOCATIONS = State()
    GET_USER_LOCATIONS = State()