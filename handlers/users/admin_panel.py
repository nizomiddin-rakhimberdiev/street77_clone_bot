from loader import dp, db
from data.config import ADMINS
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from states.all_states import AddCategoryState
from keyboards.default.default_keyboards import admin_menu
from keyboards.inline.inline_keyboards import get_categories_btn


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in ADMINS



@dp.message_handler(AdminFilter(), commands=['start'])
async def start_admin(message: types.Message):
    await message.answer("Admin menu", reply_markup=admin_menu)




@dp.message_handler(AdminFilter(), text='Add category')
async def add_category(message: types.Message):
    await message.answer('Kategoriya nomini kiriting: ')
    await AddCategoryState.name.set()


@dp.message_handler(state=AddCategoryState.name)
async def add_category(message: types.Message, state: FSMContext):
    try:
        name = message.text
        await state.update_data(name=name)
        data = await state.get_data()
        category_name = data['name']
        db.add_category(category_name)
        await message.answer(f"Categories jadvaliga {category_name} qo'shildi")
        await state.finish()
    except Exception as e:
        await message.answer(f"Bu kategoriya mavjud, boshqa nom kiriting")
        


@dp.message_handler(text="Get category")
async def get_categories(message: types.Message):
    await message.answer("Kategoriyalar:", reply_markup=await get_categories_btn())

    