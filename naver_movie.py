import requests
from bs4 import BeautifulSoup


def movie_scraping():
    URL = 'https://movie.naver.com/movie/running/current.nhn'
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    current_movie = soup.select(
        'div[id=wrap] > div[id=container] > div[id=content] > div[class=article] > div[class=obj_section] > div[class=lst_wrap] > ul[class=lst_detail_t1] > li'
    )

    for movie in current_movie:
        a_tag = movie.select_one('dl > dt > a')

        movie_title = a_tag.contents[0]
        movie_code = a_tag['href'].split('code=')[1]

        print('title :', movie_title, '\n', 'code :', movie_code, '\n')


movie_scraping()