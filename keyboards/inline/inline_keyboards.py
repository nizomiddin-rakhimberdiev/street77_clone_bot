from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def get_categories_btn():
    categories = db.get_categories()

    categories_btn = InlineKeyboardMarkup(row_width=2)

    btns = []
    for category in categories:
        btns.append(InlineKeyboardButton(category[1], callback_data=f'category_{category[0]}'))

    categories_btn.add(*btns)
    return categories_btn


async def get_products_btn(category_id):
    products = db.get_products(category_id)

    products_btn = InlineKeyboardMarkup(row_width=2)

    btns = []
    for product in products:
        btns.append(InlineKeyboardButton(product[1], callback_data=f'product_{product[0]}'))

    products_btn.add(*btns)
    return products_btn
