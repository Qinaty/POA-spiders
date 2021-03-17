from json import loads

from bs4 import BeautifulSoup
import json
from src.base import *
from src.db_info import *

# 构建映射url->article
_url2atc = dict()


class NPRURLManager(BaseURLManager):

    def __init__(self, start_page=1, end_page=-1):
        super().__init__(start_page, end_page)

    def parse(self, page_cnt) -> list:
        # 构造目录页json
        dir_json ={
            "requests": [
                {
                    "indexName": "nprorg",
                    "params": f"query=China&maxValuesPerFacet=10&page={page_cnt-1}&analytics=true&analyticsTags=%5B%22npr.org%2Fsearch%22%5D&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&filters=&facets=%5B%22hasAudio%22%2C%22lastModifiedDate%22%2C%22shows%22%5D&tagFilters="
                },
                {
                    "indexName": "station",
                    "params": f"query=China&hitsPerPage=3&maxValuesPerFacet=10&page={page_cnt-1}&analytics=true&analyticsTags=%5B%22npr.org%2Fsearch%22%5D&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&filters=&facets=%5B%22hasAudio%22%2C%22lastModifiedDate%22%2C%22shows%22%5D&tagFilters="
                }
              ]
          }
        # 构造目录页url
        dir_url = 'https://o2dg6462xl-dsn.algolia.net/1/indexes/*/queries?x-algolia-application-id=O2DG6462XL&x-algolia-api-key=40f2ee3bc56fa66dd5551ca1496ff941'
        # 获取目录页html
        html = post_html(dir_url, dir_json).decode()
        res = loads(html)['results'][0]['hits']
        urls = []
        for i in res:
            url = 'https://www.npr.org' + i['url']
            act = Article(
                publisher='NPR',
                url='https://www.npr.org' + i['url'],
                title=i['title'],
                date=i['displayDate']['dateTime'],
                author=None, # 这一项交给NPRSpider填
                content=None,  # 这一项交给NPRSpider填
                abstract=i['bodyText'],
                location=None,
                #section=i['tags'],
                #category=i['topics'],
                section=None,
                category=None,
                pic_url=i['image']['url'] if i['image']!={} else None,
                type=i['type']
            )
            _url2atc[url] = act

            urls.append(url)

        return urls


class NPRSpider(BaseSpider):
    def __init__(self, server: str, database: str, url_manager: BaseURLManager, maximum=-1):
        super().__init__(server, database, url_manager, maximum)

    def parse(self, url) -> Article:
        html = get_html(url)
        # 构造解析器
        soup = BeautifulSoup(html, features="html.parser")
        # 获取内容
        raw_text = soup.find('div', attrs={'id':'storytext'}).find_all('p', recursive=False)
        author = soup.find('p', attrs={'class':'byline__name byline__name--block'})
        if author:
            author = author.text.strip()
        text = ''
        for i in raw_text:
            text += f'{i.text}\n'
        atc = _url2atc[url]
        atc.content = text
        atc.author = author
        del _url2atc[url]
        return atc


if __name__ == '__main__':
    um = NPRURLManager()
    spider = NPRSpider(
        server=SERVER,
        database=DATABASE,
        url_manager=um,
    )

    spider.run()
