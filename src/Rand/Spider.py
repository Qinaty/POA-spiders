from bs4 import BeautifulSoup

from src.base import *


def _blog_handler(soup: BeautifulSoup):
    # 获取文档标题
    raw_title = soup.find('title')
    title = letters(raw_title.text)
    # 获取文档内容
    raw_text = soup.find_all('p')
    text = ''
    for i in raw_text:
        text += f'{i.text}\n'
    return title, text


class RandSpider(BaseSpider):

    def __init__(self, dir_: str, url_manager: BaseURLManager, maximum=-1):
        super().__init__(dir_, url_manager, maximum)

    def _parse(self, url) -> (str, str):
        html = get_html(url)
        # 构造解析器
        soup = BeautifulSoup(html, features="html.parser")
        # 获取文章类型
        doc_type = soup.find('meta', attrs={'name': 'rand-content-type'})['content']
        # 根据类型，将解析器传给对应的Handler
        print(doc_type)
        if doc_type == 'blog':
            return _blog_handler(soup)
