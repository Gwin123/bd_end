from peewee import *

db = SqliteDatabase(r'D:\bd_end\database\people.db')


class AnimeTable(Model):
    name = TextField()
    year = IntegerField()
    rating = FloatField()
    status = TextField()
    genre = TextField()
    episodes = TextField()
    time = TextField()
    studio = TextField()
    description = TextField()
    img = TextField()

    class Meta:
        database = db


class Bookmarks(Model):
    user_id = IntegerField()
    anime_id = IntegerField()

    class Meta:
        database = db


class User(Model):
    user_id = AutoField()
    name = TextField()
    user_id_tg = TextField()
    role = TextField()

    class Meta:
        database = db


class GenreSearcher(Model):
    genre_id = IntegerField()
    anime_id = IntegerField()

    class Meta:
        database = db


class Genre(Model):
    name = TextField()

    class Meta:
        database = db


def create_all_tables():
    AnimeTable.create_table()
    Bookmarks.create_table()
    User.create_table()
    Genre.create_table()
    GenreSearcher.create_table()


def delete_all_tables():
    AnimeTable.drop_table()
    Bookmarks.drop_table()
    User.drop_table()
    Genre.drop_table()
    GenreSearcher.drop_table()


def reload_all():
    create_all_tables()
