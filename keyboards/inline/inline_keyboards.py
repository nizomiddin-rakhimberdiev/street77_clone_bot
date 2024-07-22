from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def get_categories_btn():
    categories = db.get_category()

    categories_btn = InlineKeyboardMarkup(row_width=2)

    btns = []
    for category in categories:
        btns.append(InlineKeyboardButton(category[1], callback_data=f'category_{category[0]}'))

    categories_btn.add(*btns)
    return categories_btn