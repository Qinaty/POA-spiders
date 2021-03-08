from json import loads
from os import mkdir

from bs4 import BeautifulSoup

from base import *


class CNNURLManager(BaseURLManager):

    def __init__(self, start_page=1, end_page=-1):
        super().__init__(start_page, end_page)

    def parse(self, page_cnt) -> list:
        # 构造目录页url
        dir_url = f'https://search.api.cnn.io/content?size=10&q=china&from={10 * (page_cnt - 1)}&page={page_cnt}'
        # 获取目录页html
        html = get_html(dir_url).decode()
        res = loads(html)['result']
        urls = []
        for i in res:
            if i['type'] == 'article':
                urls.append(i['url'])
        return urls


class CNNSpider(BaseSpider):
    def __init__(self, dir_: str, url_manager: BaseURLManager, maximum=-1):
        super().__init__(dir_, url_manager, maximum)

    def parse(self, url) -> (str, str):
        html = get_html(url)
        # 构造解析器
        soup = BeautifulSoup(html, features="html.parser")
        # 获取标题
        raw_title = soup.find('title').text
        title = letters(raw_title)
        # 获取内容
        raw_text = soup.find_all('div', attrs={'class': 'zn-body__paragraph'})
        text = ''
        for i in raw_text:
            text += f'{i.text}\n'
        return title, text


if __name__ == '__main__':
    path = './results/CNN'

    try:
        mkdir(path)
    except FileExistsError:
        pass

    um = CNNURLManager()
    spider = CNNSpider(dir_=path, url_manager=um, maximum=100)

    spider.run()
