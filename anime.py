class Anime:
    def __init__(self, name, year, rating, status, genre, edisods, time, studio, description, img):
        self.name = name
        self.year = int(year)
        self.rating = float(rating)
        self.status = status
        self.genre = genre
        self.description = description
        self.episods = edisods
        self.time = time
        self.studio = studio
        self.img = img

    def __repr__(self):
        return f'Название аниме: {self.name} \n' \
               f'Год премьеры: {self.year}\n' \
               f'Рейтинг: {self.rating}/10 \n' \
               f'Статус: {self.status} \n' \
               f'Жанр: {self.genre} \n' \
               f'Время серии: {self.time} \n' \
               f'Студия: {self.studio}\n' \
               f'Количество эпизодов: {self.episods}\n' \
               f'Описание: {self.description}\n' \
               f'Ссылка: {self.img}'

    def __str__(self):
        return f'<b>Название аниме:</b> {self.name} \n \n' \
               f'<b>Год премьеры:</b> {self.year}\n \n' \
               f'<b>Рейтинг:</b> {self.rating}/10 \n \n' \
               f'<b>Статус:</b> {self.status} \n \n' \
               f'<b>Жанр:</b> {self.genre} \n \n' \
               f'<b>Время серии:</b> {self.time} \n \n' \
               f'<b>Студия:</b> {self.studio}\n \n' \
               f'<b>Количество эпизодов:</b> {self.episods}\n \n' \
               f'<b>Описание:</b> {self.description}\n'

    def get_info_from_anime(self) -> tuple:
        return (self.name, self.year, self.rating, self.status,
                str(self.genre), self.episods, self.time,
                self.studio, self.description, self.img)

    def get_genre(self) -> list:
        genrys = self.genre[2:len(self.genre) - 2:]
        genrys = genrys.replace(',', '')

        return genrys.split()
