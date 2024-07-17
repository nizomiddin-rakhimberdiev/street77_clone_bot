from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterState(StatesGroup):
    language = State()
    city = State()