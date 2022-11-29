import datetime
import requests
from bs4 import BeautifulSoup
from utils.excels_func import create_excel
from utils.converter import rub_to_usd

url = 'https://auto.drom.ru/audi/all/?minprice=250000&maxprice=1200000&minyear=2000&transmission[]=1&fueltype=2&mv=1.9&xv=2.7'
urls = [url[:29] + f'/page{i}' + url[29:] for i in range(1, 10)]

def parse_drop_ru():
    cost_1_rub = rub_to_usd()
    cars = []
    cars.append(('brand',
                 'model',
                 'body',
                 'year',
                 'price_rub',
                 'price_usd',
                 'transmission',
                 'volume',
                 'engine',
                 'type_body',
                 'kilometre',
                 'url'))

    for url in urls[:5]:
        try:
            page = requests.get(url)
            time = datetime.datetime.now()
            soup = BeautifulSoup(page.content, "lxml")
            # print(soup)
            print(datetime.datetime.now() - time)
            div_cars = soup.find('div', {'id': 'tabs'}).find_next_sibling('div').find('div')
            div_cars = div_cars.find('div').find_all('a')
            for soup_item in div_cars:
                div_items = soup_item.find('div').find_next_siblings('div')
                name = div_items[0].find('span', {'data-ftid': 'bull_title'}).text
                brand, model, year = name[:4], name[5:-6], name[-4:]
                params = div_items[0].find('div').find_next_sibling('div').text
                list_params = params[18:].split(', ')[:4]
                list_params = list_params if len(list_params) == 4 else list_params+['']
                volume, engine, transmission, trash, kilometre = params[:3], *list_params
                car_url = soup_item.get("href")
                price_rub = soup_item.find('span', {'data-ftid': 'bull_price'}).text
                price_rub = int(price_rub.replace('\xa0', ''))
                price_usd = round(price_rub * cost_1_rub)
                cars.append(
                    (brand,
                     model,
                     None,
                     year,
                     price_rub,
                     price_usd,
                     transmission,
                     volume,
                     engine,
                     None,
                     kilometre.replace('тыс.', '000'),
                     car_url))
        except Exception as e:
            print(e)

    create_excel('cars', 'ru', cars)


if __name__ == '__main__':
    parse_drop_ru()
