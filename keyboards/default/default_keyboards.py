from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


languages = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇺🇿 O'zbekcha")
        ],
        [
            KeyboardButton(text="🇬🇧 English")
            ]
        ],
        resize_keyboard=True
)


cities = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Toshkent"),
            KeyboardButton(text="Andijon")
        ],
        [
            KeyboardButton(text="Samarqand")
            ]
        ],
        resize_keyboard=True
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍽 Menyu"),
        ],
        [
            KeyboardButton(text="📖 Buyurtmalar tarixi"),
            KeyboardButton(text="✍️ Fikr bildirish"),
        ],
        [
            KeyboardButton(text="ℹ️ Ma'lumot"),
            KeyboardButton(text="☎️ Biz bilan aloqa"),
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar"),
        ],
    ],
    resize_keyboard=True,
)