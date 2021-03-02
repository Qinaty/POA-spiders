import os
from bs4 import BeautifulSoup

from .url_manager import URLManager
from .utility import *


class Spider:
    """
    从URLManager处获取url并解析，将内容存储到本地
    """
    def __init__(self, dir_: str, maximum=-1, start_page=1, end_page=-1):
        """
        :param dir_: 文档存储路径
        :param maximum: 爬取的最大文章数，默认为无穷
        :param start_page: 见url_manager.py
        :param end_page: 同上
        """
        self.dir_ = dir_
        self.maximum = maximum
        self._url_manage = URLManager(start_page, end_page)
        self._logger = get_logger('Spider')

    def run(self):
        self._logger.debug('Started running')
        # 开启url管理器
        self._url_manage.run()
        cnt = 0
        all_classes = set()
        # 循环爬取
        while True:

            # 达到最大爬取数时退出
            if cnt == self.maximum:
                self._logger.debug('Counted to maximum')
                break
            # 当url管理器为空时，分情况讨论
            elif self._url_manage.is_empty:
                # url管理器还在工作，等待其填充url
                if self._url_manage.is_working:
                    while self._url_manage.is_empty:
                        pass
                # 没有在工作，说明已没有内容可供爬取，退出
                else:
                    self._logger.debug(f'No resources are available')
                    break
            cnt += 1

            url = self._url_manage.new_url()
            self._logger.debug(f'New url: {url}')
            html = get_html(url)
            # 构造解析器
            soup = BeautifulSoup(html, features="html.parser")
            # 获取文章类型
            doc_type = soup.find(attrs={'name': 'rand-content-type'})['content']
            # 根据类型，将解析器传给对应的Handler
            if doc_type == 'blog':
                self._blog_handler(soup)
            elif doc_type == 'brochure':
                self._brochure_handler(soup)
            elif doc_type == 'commentary':
                self._commentary_handler(soup)
            elif doc_type == 'journal article':
                self._journal_article_handler(soup)
            elif doc_type == 'multimedia':
                self._multimedia_handler(soup)
            elif doc_type == 'news release':
                self._news_release_handler(soup)
            elif doc_type == 'report':
                self._report_handler(soup)
            elif doc_type == 'testimony':
                self._testimony_handler(soup)
            else:
                self._logger.warning(f'Found new document type: {doc_type}')

        self._logger.debug('Done')

    def _blog_handler(self, soup: BeautifulSoup):
        # 获取文档标题
        raw_title = soup.find('title')
        # 获取文档所有段落
        raw_texts = soup.find_all('p')
        # 构建文档存储路径
        title = letters(raw_title.text)
        path = f'{os.path.join(self.dir_, title)}.txt'
        # 将所有段落写入文档
        with open(path, 'w') as f:
            for rt in raw_texts:
                text = rt.text
                f.write(f'{text}\n')

    def _brochure_handler(self, soup: BeautifulSoup):
        pass

    def _commentary_handler(self, soup: BeautifulSoup):
        pass

    def _journal_article_handler(self, soup: BeautifulSoup):
        pass

    def _multimedia_handler(self, soup: BeautifulSoup):
        pass

    def _news_release_handler(self, soup: BeautifulSoup):
        pass

    def _report_handler(self, soup: BeautifulSoup):
        pass

    def _testimony_handler(self, soup: BeautifulSoup):
        pass

