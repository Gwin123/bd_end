from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from callbacks.calldata import BookmarkCallback, GenreCallback


def calc_kb():
    items = [
        '1', '2', '3', '+',
        '4', '5', '6', '-',
        '7', '8', '9', '*',
        '0', '.', '=', '/'
    ]

    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.button(text=item)

    builder.button(text="Назад")

    return builder.as_markup(resize_keyboard=True)


def genres_kb():
    from database.request import get_all_genres

    items = get_all_genres()

    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=item, callback_data=GenreCallback(type="choose_genre", genre_name=item))

    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True)


def generate_bookmark_keyboard(text, foo, id):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=text, callback_data=BookmarkCallback(type="bookmark", description=foo, id=id).pack())
    ]])
