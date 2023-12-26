from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Paginator(CallbackData, prefix='pag'):
    action: str
    page: int


def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="<=", callback_data=Paginator(action='prev', page=page).pack()),
        InlineKeyboardButton(text="=>", callback_data=Paginator(action='next', page=page).pack()),
    )
    return builder.as_markup()
