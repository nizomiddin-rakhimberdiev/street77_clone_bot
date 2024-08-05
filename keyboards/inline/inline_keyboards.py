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


async def get_basket_keyboard(product_id, count):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("-", callback_data=f"decrement:{product_id}"),
        InlineKeyboardButton(f"{count}", callback_data=f"count:{product_id}"),
        InlineKeyboardButton("+", callback_data=f"increment:{product_id}")
    )
    keyboard.add(
        InlineKeyboardButton("Savatga qo'shish", callback_data=f"add_to_cart:{product_id}")
    )
    return keyboard
