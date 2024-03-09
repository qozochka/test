from aiogram.fsm.state import StatesGroup, State


class SearchForm(StatesGroup):
    GET_CITY = State()
    GET_DISTRICT = State()
    GET_STREET = State()