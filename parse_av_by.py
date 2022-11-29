import datetime

import requests
from bs4 import BeautifulSoup
from utils.excels_func import create_excel
from utils.converter import byn_to_usd

url = 'https://cars.av.by/filter?brands[0][brand]=6&year[min]=2000&price_usd[min]=3000&price_usd[max]=15000&engine_capacity[min]=1900&engine_capacity[max]=2700&transmission_type=2&engine_type[0]=5&place_region[0]=1003&place_region[1]=1006&place_region[2]=1005'
urls = [
    'https://cars.av.by/filter?brands[0][brand]=6&year[min]=2000&price_usd[min]=3000&price_usd[max]=15000&engine_capacity[min]=1900&engine_capacity[max]=2700&transmission_type=2&engine_type[0]=5&place_region[0]=1003&place_region[1]=1006&place_region[2]=1005'
]

urls = [url + f'&page={i}' for i in range(1, 10)]


def parse_av_by():
    cost_1_byn = byn_to_usd()
    cars = []
    cars.append(('brand',
                 'model',
                 'body',
                 'year',
                 'price_byn',
                 'price_usd',
                 'transmission',
                 'volume',
                 'engine',
                 'type_body',
                 'kilometre',
                 'url'))
    for url in urls[:3]:
        time = datetime.datetime.now()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")
        print(datetime.datetime.now() - time)
        div_cars = soup.find_all(class_='listing-item')
        for soup_item in div_cars:
            name = soup_item.find('div', class_='listing-item__about').find('span', class_='link-text').text.split(' ')
            brand, model, body = name[0], name[1], ' '.join([_ for _ in name[2:] if _ != '·'])
            params = soup_item.find('div', class_='listing-item__params').find_all('div')
            ptvet = params[1].text.split(', ')
            year, transmission, volume, engine, type_body, kilometre = params[0].text[:-3], ptvet[0], ptvet[1][:-2], \
                                                                       ptvet[2], ptvet[3], params[2].text
            price_byn = soup_item.find('div', class_='listing-item__price').text
            price_byn = int(price_byn[:-3].replace(' ', '').replace('\u2009', ''))
            price_usd = round(price_byn * cost_1_byn)
            car_url = 'https://cars.av.by' + soup_item.find('a', class_='listing-item__link').get('href')
            cars.append((brand,
                         model,
                         body,
                         year,
                         price_byn,
                         price_usd,
                         transmission,
                         volume,
                         engine,
                         type_body,
                         kilometre,
                         car_url))
    create_excel('cars', 'by', cars)


if __name__ == '__main__':
    parse_av_by()
