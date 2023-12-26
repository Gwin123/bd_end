from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from constants.const import SEARCH, TOP, GENRES, BOOKMARKS, SETTINGS

main_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=SEARCH)
    ],

    [
        KeyboardButton(text=SETTINGS),
        KeyboardButton(text=GENRES)
    ],

    [
        KeyboardButton(text=BOOKMARKS)
    ],

], resize_keyboard=True)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Выгрузить данные"),
            KeyboardButton(text="Создать backup"),
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

convert_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Json"),
            KeyboardButton(text="CSV"),
        ],
        [
            KeyboardButton(text="Excel")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ], resize_keyboard=True
)


search_settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="По жанрам"),
            KeyboardButton(text="По годам"),
        ],
        [
            KeyboardButton(text="По студии"),
            KeyboardButton(text="По рейтингу")
        ],
        [
            KeyboardButton(text="Назад")

        ]
    ], resize_keyboard=True
)