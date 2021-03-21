from os import mkdir

from bs4 import BeautifulSoup

from base import *


class RandURLManager(BaseURLManager):

    def __init__(self, start_page=1, end_page=-1):
        super().__init__(start_page, end_page)

    def parse(self, page_cnt) -> list:
        # 构造目录页url
        dir_url = f'https://www.rand.org/topics/china.html?page={page_cnt}'
        # 获取目录页html
        html = get_html(dir_url)
        # 构造解析器
        soup = BeautifulSoup(html, features="html.parser")
        # 找到teasers list organic类下所有类名为title的tag
        raw_urls = soup.find(attrs={'class': 'teasers list organic'}).find_all(attrs={'class': 'title'})
        # 如果没有找到匹配的结果，说明已经爬取完毕，退出循环
        urls = []
        for i in raw_urls:
            # 子tag中的href属性
            url = i.contents[0]['href']
            urls.append(url)
        return urls


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

    def parse(self, url) -> (str, str):
        html = get_html(url)
        # 构造解析器
        soup = BeautifulSoup(html, features="html.parser")
        # 获取文章类型
        doc_type = soup.find('meta', attrs={'name': 'rand-content-type'})['content']
        # 根据类型，将解析器传给对应的Handler
        if doc_type == 'blog':
            return _blog_handler(soup)


if __name__ == '__main__':
    path = './results/Rand'

    try:
        mkdir(path)
    except FileExistsError:
        pass

    um = RandURLManager()
    spider = RandSpider(dir_=path, url_manager=um, maximum=10)

    spider.run()
