from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from constants.const import ADMIN_ID
from database.request import is_user_reg, add_user, get_user_role
from keyboards import reply
from keyboards.reply import admin_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>! "
                         f"Это бот для поиска аниме. Хорошего просмотра.", reply_markup=reply.main_kb)

    if not is_user_reg(message.from_user.id):
        add_user(message.from_user.username, message.from_user.id,
                 "user" if message.from_user.id != ADMIN_ID else "admin")


@router.message(Command('admin'))
async def admin_tools(message: Message):
    if get_user_role(message.from_user.id) == 'admin':
        await message.answer("Режим админа включён", reply_markup=admin_menu)
    else:
        await message.answer("Откуда ты узнал эту команду? 👨‍💻")
