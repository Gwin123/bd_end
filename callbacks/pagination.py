from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.calldata import MyCallback, GenreCallback, BookmarkCallback
from constants.const import ADD_BOOKMARK, DELETE_BOOKMARK
from database.request import get_anime_from_id, get_anime_ids_from_genre_name, is_bookmark_in, add_bookmark, \
    delete_from_bookmark, get_ids_anime_from_studio, get_ids_anime_from_year
from keyboards.builders import generate_bookmark_keyboard

router = Router()


@router.callback_query(GenreCallback.filter(F.type == "choose_genre"))
async def send_anime_of_genre(call: CallbackQuery, callback_data: GenreCallback):
    genre_name = callback_data.genre_name

    anime_ids = get_anime_ids_from_genre_name(genre_name)

    buttons = []
    for anime_id in anime_ids:
        anime = get_anime_from_id(anime_id)

        button = InlineKeyboardButton(text=anime.name,
                                      callback_data=MyCallback(foo="send", bar=str(anime_id)).pack())
        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if len(buttons) > 0:
        text = f'Вот, что удалось найти по запросу "{genre_name}"'
    else:
        text = f'Ничего не найдено по запросу "{genre_name}"'

    await call.message.answer(text=text, reply_markup=kb)
    await call.answer()


@router.callback_query(MyCallback.filter(F.foo == "studio"))
async def send_anime_of_studio(call: CallbackQuery, callback_data: MyCallback):
    studio_name = callback_data.bar

    anime_ids = get_ids_anime_from_studio(studio_name)

    buttons = []
    for anime_id in anime_ids:
        anime = get_anime_from_id(anime_id)

        button = InlineKeyboardButton(text=anime.name,
                                      callback_data=MyCallback(foo="send", bar=str(anime_id)).pack())
        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await call.message.answer(text=studio_name, reply_markup=kb)
    await call.answer()


@router.callback_query(MyCallback.filter(F.foo == "year"))
async def send_anime_of_year(call: CallbackQuery, callback_data: MyCallback):
    year_1, year_2 = map(int, callback_data.bar.split('-'))

    anime_ids = get_ids_anime_from_year(year_1, year_2)

    buttons = []
    for anime_id in anime_ids:
        anime = get_anime_from_id(anime_id)

        button = InlineKeyboardButton(text=anime.name,
                                      callback_data=MyCallback(foo="send", bar=str(anime_id)).pack())
        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await call.message.answer(text=callback_data.bar, reply_markup=kb)
    await call.answer()


@router.callback_query(MyCallback.filter(F.foo == "send"))
async def send_anime(call: CallbackQuery, callback_data: MyCallback) -> None:
    anime_id = int(callback_data.bar)
    anime = get_anime_from_id(anime_id)

    if is_bookmark_in(anime_id, call.from_user.id):
        text, foo = DELETE_BOOKMARK, 0
    else:
        text, foo = ADD_BOOKMARK, 1

    kb_bookmark = generate_bookmark_keyboard(text, foo, anime_id)

    await call.message.answer_photo(anime.img, str(anime), reply_markup=kb_bookmark)
    await call.answer()


@router.callback_query(BookmarkCallback.filter(F.type == "bookmark"))
async def add_anime_to_bookmarks(call: CallbackQuery, callback_data: BookmarkCallback) -> None:
    id = callback_data.id

    is_bookmark_in(id, call.from_user.id)

    if callback_data.description:
        add_bookmark(id, call.from_user.id)

        text = DELETE_BOOKMARK
    else:
        delete_from_bookmark(id, call.from_user.id)

        text = ADD_BOOKMARK

    kb_bookmark = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=text,
                             callback_data=BookmarkCallback(type="bookmark",
                                                            description=bool(not callback_data.description),
                                                            id=id).pack())
    ]])

    await call.message.edit_reply_markup(call.inline_message_id, kb_bookmark)

    await call.answer()
