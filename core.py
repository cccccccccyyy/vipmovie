import requests
from bs4 import BeautifulSoup


def get_vip_url():
    url = 'https://www.niudh.cn/tools/vip/'
    res = requests.get(url).text
    html = BeautifulSoup(res, 'html.parser')
    return [option['value'] for option in html.select('option')][0]
