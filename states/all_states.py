from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterState(StatesGroup):
    language = State()
    city = State()


class AddCategoryState(StatesGroup):
    name = State()