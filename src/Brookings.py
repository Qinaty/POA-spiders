from json import loads

from bs4 import BeautifulSoup

from src.base import *
from src.db_info import *

# 构建映射url->article
_url2atc = dict()

class BRKURLManager(BaseURLManager):

    def __init__(self, start_page=1, end_page=-1):
        super().__init__(start_page, end_page)

    def parse(self, page_cnt) -> list:
        # 构造目录页url
        year = 2020
        dir_url = f'https://www.csis.org/search?search_api_views_fulltext=China&sort_by=field_publication_date&field_publication_date={year}&page={page_cnt-1}'
        # 获取目录页html
        html = get_html(dir_url).decode()
        soup = BeautifulSoup(html, features="html.parser")
        res = soup.find_all('article', attrs={'class':'teaser teaser--search-result'})
        urls = []
        for i in res:
            tit = i.find('div', attrs={'class':'teaser__title'}).find('a')
            url = 'https://www.csis.org' + tit['href']
            title = tit.text
            try:
                date = i.find('span', attrs={'teaser__date'}).find('span')['content']
            except:
                date = None
            try:
                abstract = i.find('div', attrs={'class': 'teaser__description'}).find('p').text
            except:
                abstract = None
            try:
                authors = i.find('span', attrs={'class': 'teaser__expert'}).find('a').text
            except:
                authors = None
            try:
                type = i.find('div', attrs={'class': 'teaser__type'}).text
            except:
                type = None

            act = Article(
                publisher='Brookings',
                url=url,
                title=title,
                date=date,
                authors=authors,
                content=None,  # 这一项交给BRKSpider填
                abstract=abstract,
                location=None,
                section=None,
                category=None, # 这一项交给BRKSpider填
                pic_url=None,
                type=type
            )
            _url2atc[url] = act
            urls.append(url)

        return urls


class BRKSpider(BaseSpider):
    def __init__(self, server: str, database: str, url_manager: BaseURLManager, maximum=-1):
        super().__init__(server, database, url_manager, maximum)

    def parse(self, url) -> Article:
        html = get_html(url)
        # 构造解析器
        soup = BeautifulSoup(html, features="html.parser")
        # 获取内容
        raw_text = soup.find('article', attrs={'role':'article'})
        text = raw_text.text

        atc = _url2atc[url]
        atc.content = text
        try:
            related = soup.find('div', attrs={'class':'field field--spaced'}).find_all('a')
            category = []
            for c in related:
                category.append(c.text)
            atc.category = str(category)
        except:
            atc.category = None
        del _url2atc[url]
        return atc


if __name__ == '__main__':
    um = BRKURLManager()
    spider = BRKSpider(
        server=SERVER,
        database=DATABASE,
        url_manager=um,
    )

    spider.run()
