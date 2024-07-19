from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.default_keyboards import languages, cities, main_menu
from states.all_states import RegisterState

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
        db_users = db.get_users_id()
        users = []
        for user in db_users:
            users.append(user[0])
        print(users)
        if message.from_user.id in users:
                await message.answer("Bosh menyu", reply_markup=main_menu)
        else:
            await message.answer("""Здравствуйте! Давайте для начала выберем язык обслуживания!

    Keling, avvaliga xizmat ko’rsatish tilini tanlab olaylik.

    Hi! Let's first we choose language of serving!""", reply_markup=languages)
            await RegisterState.language.set()


@dp.message_handler(lambda msg: msg.text in ["🇷🇺 Русский", "🇺🇿 O'zbekcha", "🇬🇧 English"],state=RegisterState.language)
async def bot_language(message: types.Message, state: FSMContext):
    language = message.text
    if language == "🇷🇺 Русский":
        await state.update_data(language='ru')
    elif language == "🇺🇿 O'zbekcha":
        await state.update_data(language='uz')
    elif language == "🇬🇧 English":
        await state.update_data(language='en')

    await message.answer(f"Siz qaysi shaharda istiqomat qilasiz?\nIltimos, shaharni tanlang:", reply_markup=cities)
    await RegisterState.city.set()



@dp.message_handler(lambda msg: msg.text in ["Toshkent", "Andijon", "Samarqand"], state=RegisterState.city)
async def bot_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)

    data = await state.get_data()
    language = data["language"]
    user_id = message.from_user.id
    db.add_user(user_id, language, city)
    await message.answer("Bosh menu", reply_markup=main_menu)
    await state.finish()