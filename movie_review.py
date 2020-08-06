import requests
from bs4 import BeautifulSoup

URL = "https://movie.naver.com/movie/running/current.nhn"

response = requests.get('https://movie.naver.com/movie/running/current.nhn')
soup = BeautifulSoup(response.text, 'html.parser')

movies_list = soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li')

final_movie_data = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag['href'].split('code=')[1]

    movie_data = {
        'title': movie_title,
        'code': movie_code
    }

    final_movie_data.append(movie_data)

headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=J6IBEEVKC7VV4; NDARK=Y; NRTK=ag#all_gr#0_ma#-2_si#-2_en#-2_sp#-2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; _ga=GA1.2.2009634825.1596117402; _gid=GA1.2.2144243518.1596612364; NV_WETR_LOCATION_RGN_M="MDkxNDAxMDQ="; NV_WETR_LAST_ACCESS_RGN_M="MDkxNDAxMDQ="; page_uid=UyXq7lp0YidssdH7TAKssssstkw-309053; NM_VIEWMODE_AUTO=basic; BMR=s=1596698072947&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dwideeyed%26logNo%3D221350638501%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; csrf_token=4c87c0af-4cc8-49bf-9005-d281ca88469c',
}

params = (
    ('code', '189069'),
    ('type', 'after'),
    ('isActualPointWriteExecute', 'false'),
    ('isMileageSubscriptionAlready', 'false'),
    ('isMileageSubscriptionReject', 'false'),
)

response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=189069&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false', headers=headers)

final_movie_data

for movie in final_movie_data:
    movie_code = movie['code']
    # print(movie_code)
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)

    review = BeautifulSoup(response.text, 'html.parser')

    review_list = review.select('body > div > div > div.score_result > ul > li ')

    final_review_list = []

    for review in review_list:
        review_rating = review.select_one('div.star_score > em').get_text()
        review_txt = review.select_one('div.score_reple > p > span').get_text().strip()
        
        movie_review_data = {
            'rating' : review_rating,
            'review' : review_txt
        }

        final_review_list.append(movie_review_data)

print(final_review_list)