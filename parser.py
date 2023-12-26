import requests as req
from bs4 import BeautifulSoup, PageElement

from anime import Anime


def get_info(anime: PageElement) -> Anime | None:
    name = anime.find('h2', class_='card__title').text
    description = anime.find('p', class_='card__text line-clamp').text
    img = 'https://animego-online.org' + anime.find('img')['src']

    info = anime.find('ul', class_='card__list').text
    info = info.split('\n')[1:-1]
    info.sort()

    formated_info = [elem[elem.find(':') + 2:] for elem in info]

    rating = 0
    rating_elem = anime.find('div', class_='card__rating-ext imdb')

    if rating_elem:
        rating = float(str(rating_elem.text).split()[0].replace(',', '.'))

    if len(formated_info) == 6:
        time, year, *genres, status, studio, episodes = formated_info
        genres = ' '.join(genres).replace('  ', ' ')
        return Anime(name, year, rating, status, genres, episodes, time, studio, description, img)
    else:
        return None


def get_all_anime(count) -> list[Anime]:
    ani_list = []
    for i in range(1, count + 1):
        resp = req.get(f'https://animego-online.org/page/{i}')
        soup = BeautifulSoup(resp.text, 'lxml')

        all_anime_data = soup.findAll('article', class_='card d-flex')
        ani_list.extend([get_info(anime) for anime in all_anime_data if get_info(anime) != None])

    return ani_list
