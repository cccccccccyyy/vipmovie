import webbrowser
from core import get_vip_url

vip_url = get_vip_url()

while True:
    movie_url = vip_url + input('请复制电影网址：')
    webbrowser.open(movie_url)
    print('已在浏览器中打开')
