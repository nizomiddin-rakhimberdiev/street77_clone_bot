from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from  loader import db


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
            KeyboardButton(text="🛍 Savat"),
            KeyboardButton(text="⚙️ Sozlamalar")
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


filial_loc = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Send locations", request_location=True)
        ]
    ]
)


async def get_filials_btn():
    filails = db.get_filials()

    filials_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton("📍 Eng yaqin filialni aniqlash")
                ]
            ],
            resize_keyboard=True,
            row_width=2)
        
    btns = []

    for filial in filails:
            print(filial)
            btns.append(KeyboardButton(text=filial[0]))

    filials_btn.add(*btns)

    return filials_btn

zakaz_turi = ReplyKeyboardMarkup(
      keyboard=[
          [
              KeyboardButton(text="🚘 Yetkazib berish"),
              KeyboardButton(text= "🏃 Olib ketish")
          ],
          [
                KeyboardButton(text= "⬅️ Ortga")
          ]
      ],
      resize_keyboard=True,
)