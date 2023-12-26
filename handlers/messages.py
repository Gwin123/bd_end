from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from backup import create_backup
from callbacks.calldata import MyCallback
from constants.const import *
from converters.csv_converter import *
from database.models import *
from database.request import get_anime_from_id, get_all_anime_ids, get_anime_id_from_user_bookmarks, has_bookmarks, \
    get_all_studios
from keyboards.builders import genres_kb
from keyboards.reply import convert_menu, main_kb, search_settings
from str_equal import is_names_equal

router = Router()


@router.message(F.text == "По жанрам")
async def genres(message: Message):
    await message.answer("Доступные жанры:", reply_markup=genres_kb())


@router.message(F.text == "Параметры 🧩")
async def top(message: Message):
    await message.answer("Настройки поиска", reply_markup=search_settings)


@router.message(F.text == "Выгрузить данные")
async def top(message: Message):
    await message.answer("Выберите формат", reply_markup=convert_menu)


@router.message(F.text == "Назад")
async def top(message: Message):
    await message.answer("Главное меню", reply_markup=main_kb)


@router.message(F.text == "По студии")
async def top(message: Message):
    all_studios = get_all_studios()
    buttons = []
    for studio in all_studios:
        button = InlineKeyboardButton(text=studio,
                                      callback_data=MyCallback(foo="studio", bar=studio).pack())
        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Студии, снимающие аниме", reply_markup=kb)


@router.message(F.text == "По годам")
async def top(message: Message):
    all_years = ['2020-2023', '2016-2019', '2012-2015',
                 '2008-2011', '2004-2007', '2000-2003',
                 '1996-1999', '1992-1995', '1988-1991']

    buttons = []
    for year_range in all_years:
        button = InlineKeyboardButton(text=year_range,
                                      callback_data=MyCallback(foo="year", bar=year_range).pack())
        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Выберите промежуток", reply_markup=kb)


@router.message(F.text == "Создать backup")
async def top(message: Message):
    await create_backup()

    await message.answer("Backup создан")


@router.message(F.text == "CSV")
async def get_data_on_csv(message: Message):
    tables = [User, AnimeTable, Bookmarks, Genre, GenreSearcher]
    tables_name = ["user", "anime", "bookmarks", "genres", "genre_searcher"]

    for i in range(len(tables)):
        write_to_csv(tables[i], f"convert/{tables_name[i]}")

    media = MediaGroupBuilder()

    for table_name in tables_name:
        media.add(type=InputMediaType.DOCUMENT, media=FSInputFile(f"convert/{table_name}.csv"))

    await message.answer_media_group(media=media.build())


@router.message(F.text == "Json")
async def get_data_on_json(message: Message):
    tables = [User, AnimeTable, Bookmarks, Genre, GenreSearcher]
    tables_name = ["user", "anime", "bookmarks", "genres", "genre_searcher"]

    for i in range(len(tables)):
        write_to_json(tables[i], f"convert/{tables_name[i]}")

    media = MediaGroupBuilder()

    for table_name in tables_name:
        media.add(type=InputMediaType.DOCUMENT, media=FSInputFile(f"convert/{table_name}.json"))

    await message.answer_media_group(media=media.build())


@router.message(F.text == "Excel")
async def get_data_on_excel(message: Message):
    tables = [User, AnimeTable, Bookmarks, Genre, GenreSearcher]
    tables_name = ["user", "anime", "bookmarks", "genres", "genre_searcher"]

    for i in range(len(tables)):
        write_to_excel(tables[i], f"convert/{tables_name[i]}")

    media = MediaGroupBuilder()

    for table_name in tables_name:
        media.add(type=InputMediaType.DOCUMENT, media=FSInputFile(f"convert/{table_name}.xlsx"))

    await message.answer_media_group(media=media.build())


@router.message(F.text == BOOKMARKS)
async def bookmarks(message: Message):
    if has_bookmarks(message.from_user.id):
        anime_ids = get_anime_id_from_user_bookmarks(message.from_user.id)
        buttons = []
        for anime_id in anime_ids:
            anime = get_anime_from_id(anime_id)

            button = InlineKeyboardButton(text=anime.name,
                                          callback_data=MyCallback(foo="send", bar=str(anime_id)).pack())
            buttons.append([button])

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(f"Ваши закладки, {message.from_user.first_name}", reply_markup=kb)
    else:
        await message.answer("Список закладок пуст")


@router.message(F.text == SEARCH)
async def search(message: Message):
    await message.answer("Просто отправьте боту название аниме")


@router.message()
async def find_anime(message: Message):
    msg_text = message.text

    all_anime_ids = get_all_anime_ids()

    buttons = []
    for anime_id in all_anime_ids:
        anime = get_anime_from_id(anime_id)

        if is_names_equal(anime.name, msg_text):
            button = InlineKeyboardButton(text=anime.name,
                                          callback_data=MyCallback(foo="send", bar=str(anime_id)).pack())
            buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if len(buttons) > 0:
        text = f'Вот, что удалось найти по запросу "{msg_text}"'
    else:
        text = f'К сожалению, по вашему запросу ничего не найдено. 😔\n \n' \
               f'Попробуйте проверить правильность написания названия фильма'

    await message.answer(text=text, reply_markup=kb)
