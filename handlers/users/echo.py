from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


# state ko'rsatilmagan barcha xabarlar uchun handler
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"state ko'rsatilmadi."
                         f"Xabar:\n"
                         f"{message.text}")


# state="*" xabarlar uchun handler
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"<code>state={state}</code>.\n"
                         f"\nXabar:\n"
                         f"<code>{message}</code>")
