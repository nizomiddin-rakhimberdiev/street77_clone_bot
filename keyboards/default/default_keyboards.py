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


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Add filial'),
            KeyboardButton(text='Add category'),
            KeyboardButton(text='Add product')
        ],
        [
            KeyboardButton(text='Get filial'),
            KeyboardButton(text='Get category'),
            KeyboardButton(text='Get product')
        ]
    ],
    resize_keyboard=True,
)