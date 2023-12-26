from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Telegram', url='tg://resolve?domain=gwin_disel')
        ]
    ]
)

