from database.models import *
from parser import get_all_anime, Anime


def add_anime_to_bd(anime: Anime) -> None:
    AnimeTable.create(name=anime.name,
                      year=anime.year,
                      rating=anime.rating,
                      status=anime.status,
                      genre=anime.genre,
                      episodes=anime.episods,
                      time=anime.time,
                      studio=anime.studio,
                      description=anime.description,
                      img=anime.img)


def get_all_genres() -> list:
    anime_genres = AnimeTable.select(AnimeTable.genre)

    genres_unique = set()
    for genres_anime in anime_genres:
        genres_anime = str(genres_anime.genre)

        all_genre = genres_anime.split(',')
        for genre in all_genre:
            genres_unique.add(genre.lower().strip())

    return sorted(list(genres_unique))


def get_anime_from_id(anime_id: int) -> Anime:
    for anime in AnimeTable.select().where(AnimeTable.id == anime_id):
        return Anime(anime.name, anime.year, anime.rating, anime.status, anime.genre, anime.episodes,
                     anime.time, anime.studio, anime.description, anime.img)


def add_genre_to_bd(genre: str) -> None:
    Genre.create(name=genre)


def add_bookmark(anime_id: int, user_id: int) -> None:
    Bookmarks.create(anime_id=anime_id, user_id=user_id)


def delete_from_bookmark(anime_id: int, user_id: int) -> None:
    Bookmarks.get(Bookmarks.anime_id == anime_id and Bookmarks.user_id == user_id).delete_instance()


def get_anime_id_from_user_bookmarks(user_id) -> list:
    anime_ids = []
    for anime in Bookmarks.select().where(Bookmarks.user_id == user_id):
        anime_ids.append(anime.anime_id)

    return anime_ids


def add_all_genre() -> None:
    all_genre = get_all_genres()
    for genre in all_genre:
        add_genre_to_bd(genre)


def upload_base() -> None:
    anime_list = get_all_anime(120)

    for anime in anime_list:
        add_anime_to_bd(anime)

    add_all_genre()


def get_id_from_genre_name(name: str) -> int:
    for genre in Genre.select(Genre.id).where(Genre.name == name):
        return genre.id


def get_all_anime_ids() -> list:
    ids = []
    for anime in AnimeTable.select(AnimeTable.id, AnimeTable.name):
        ids.append(anime.id)

    return ids


def get_anime_ids_from_genre_name(genre_name: str):
    genre_id = get_id_from_genre_name(genre_name)

    return [anime.anime_id for anime in
            GenreSearcher.select(GenreSearcher.anime_id).where(GenreSearcher.genre_id == genre_id)]


def is_bookmark_in(anime_id: int, user_id: int) -> bool:
    is_in = False
    for _ in Bookmarks.select().where((Bookmarks.anime_id == anime_id) & (Bookmarks.user_id == user_id)):
        is_in = True

    return is_in


def is_user_reg(user_id: int) -> bool:
    is_reg = False
    for _ in User.select().where(User.user_id_tg == user_id):
        is_reg = True

    return is_reg


def get_user_role(user_id: int) -> str:
    for user in User.select(User.role).where(User.user_id_tg == user_id):
        return user.role


def add_user(name: str, user_id_tg: int, role: str) -> None:
    User.create(name=name, user_id_tg=user_id_tg, role=role)


def has_bookmarks(user_id: int) -> bool:
    has = False
    for _ in Bookmarks.select().where(Bookmarks.user_id == user_id):
        has = True

    return has


def create_search_table() -> None:
    a = AnimeTable.select(AnimeTable.id, AnimeTable.genre)

    for anime in a:
        anime_id = anime.id
        genres_name = [genre.lower().strip() for genre in str(anime.genre).split(',')]

        for genre_name in genres_name:
            genre_id = get_id_from_genre_name(genre_name)
            GenreSearcher.create(genre_id=genre_id, anime_id=anime_id)


def reload_base() -> None:
    delete_all_tables()
    create_all_tables()

    upload_base()


def get_all_studios():
    studios = set()

    for studio in AnimeTable.select(AnimeTable.studio):
        studios.add(studio.studio.split(',')[0])

    return list(sorted(studios))


def get_ids_anime_from_studio(name: str) -> list:
    anime_ids = []
    for anime in AnimeTable.select(AnimeTable.id, AnimeTable.studio):
        studio = anime.studio.split(',')[0]
        if studio == name:
            anime_ids.append(anime.id)

    return anime_ids


def get_ids_anime_from_year(year_1: int, year_2: int) -> list:
    anime_ids = []
    for anime in AnimeTable.select(AnimeTable.id).where((AnimeTable.year >= year_1) & (AnimeTable.year <= year_2)):
        anime_ids.append(anime.id)

    return anime_ids


if __name__ == "__main__":
    # reload_base()
    #
    # create_search_table()

    # for anime_id in get_anime_ids_from_genre_name("комедия"):
    #     print(get_anime_from_id(anime_id))
    print(len(get_all_anime_ids()))
