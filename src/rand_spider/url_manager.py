"""
URLManager定义文件
"""
from threading import Thread
from bs4 import BeautifulSoup

from .utility import *


class URLManager:
    """
    从目录页获取文章URL，为Spider提供待爬取的URL
    """

    def __init__(self, start_page=1, end_page=-1):
        """
        初始化
        注意：每个目录页包含多个url
        :param start_page:开始目录页码
        :param end_page:结束目录页码, 默认为无穷
        """
        self.start_page = start_page
        self.end_page = end_page
        # url队列
        self.queue = list()
        # 工作状态
        self.is_working = False
        self._logger = get_logger('URLManager')

    @property
    def is_empty(self) -> bool:
        """
        :return: URL队列是否为空
        """
        return len(self.queue) == 0

    def new_url(self):
        """
        :return: 队首url
        """
        if self.is_empty:
            self._logger.warning('Get url from an empty queue.')
        else:
            return self.queue.pop(0)

    def run(self):
        """
        新开线程爬取可用url，不影响主线程运行
        :return:
        """
        self.is_working = True
        self._logger.debug('Started running')
        Thread(target=self._gather_urls, daemon=True).start()

    def _gather_urls(self):
        """
        私有方法，不可被外部调用
        :return:
        """
        # 记录当前正在爬取的目录页
        page_cnt = self.start_page
        while page_cnt != self.end_page:
            self._logger.debug(f'Parsing page {page_cnt}')
            # 构造目录页url
            dir_url = f'https://www.rand.org/topics/china.html?page={page_cnt}'
            # 获取目录页html
            html = get_html(dir_url)
            # 构造解析器
            soup = BeautifulSoup(html, features="html.parser")
            # 找到teasers list organic类下所有类名为title的tag
            raw_tags = soup.find(attrs={'class': 'teasers list organic'}).find_all(attrs={'class': 'title'})
            # 如果没有找到匹配的结果，说明已经爬取完毕，退出循环
            if len(raw_tags) == 0:
                break
            for t in raw_tags:
                # 获取t第一个子tag中的href属性
                url = t.contents[0]['href']
                # 将获取到的url加入队列
                self.queue.append(url)
            page_cnt += 1
        self.is_working = False
        self._logger.debug('Done')
