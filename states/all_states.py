from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterState(StatesGroup):
    language = State()
    city = State()


class AddCategoryState(StatesGroup):
    name = State()


class AddFilialState(StatesGroup):
    name = State()
    lat_long = State()


class AddProductState(StatesGroup):
    name = State()
    price = State()
    description = State()
    image = State()
    category_id = State()


class GetProductState(StatesGroup):
    category = State()
    product = State()

class YetkazishState(StatesGroup):
    lokatsiya = State()
    category = State()
    product = State()
    savat = State()