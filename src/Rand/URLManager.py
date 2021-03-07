"""
URLManager定义文件
"""

from bs4 import BeautifulSoup

from src.base import *


class RandURLManager(BaseURLManager):

    def __init__(self, start_page=1, end_page=-1):
        super().__init__(start_page, end_page)

    def _parse(self, page_cnt) -> list:
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
