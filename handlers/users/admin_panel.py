from loader import dp, db
from data.config import ADMINS
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from keyboards.default.default_keyboards import admin_menu


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in ADMINS



@dp.message_handler(AdminFilter(), commands=['start'])
async def start_admin(message: types.Message):
    status = AdminFilter()
    print(status.check(message))
    await message.answer("Admin menu", reply_markup=admin_menu)