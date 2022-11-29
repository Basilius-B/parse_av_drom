import requests
import re


def get_value(link):
    page = requests.get(link)
    value = re.search(r'<input id=\"to_input_curr\" type=\"text\" value=\"([\d.]+)\">', page.text).group(1)
    return float(value)


def rub_to_usd():
    return get_value('https://myfin.by/converter/rub-usd')


def byn_to_usd():
    return get_value('https://myfin.by/converter/byn-usd')
