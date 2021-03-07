"""
URLManager定义文件
"""

from json import loads

from src.base import *


class CNNURLManager(BaseURLManager):

    def __init__(self, start_page=1, end_page=-1):
        super().__init__(start_page, end_page)

    def _parse(self, page_cnt) -> list:
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
