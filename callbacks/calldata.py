from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: str


class GenreCallback(CallbackData, prefix="genre"):
    type: str
    genre_name: str


class BookmarkCallback(CallbackData, prefix="book"):
    type: str
    description: int
    id: int
