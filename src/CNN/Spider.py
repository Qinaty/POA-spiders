from bs4 import BeautifulSoup

from src.base import *


class CNNSpider(BaseSpider):
    def __init__(self, dir_: str, url_manager: BaseURLManager, maximum=-1):
        super().__init__(dir_, url_manager, maximum)

    def _parse(self, url) -> (str, str):
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
