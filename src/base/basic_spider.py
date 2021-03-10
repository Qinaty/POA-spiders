"""
BaseSpider定义文件
"""

import os
from abc import abstractmethod

from .basic_url_manager import BaseURLManager
from .utility import *


class BaseSpider:
    """
    从URLManager处获取url并解析，将内容存储到本地
    """

    def __init__(self, dir_: str, url_manager: BaseURLManager, maximum=-1):
        """
        :param dir_: 文档存储路径
        :param url_manager: URL管理器
        :param maximum: 爬取的最大文章数，默认为无穷
        """
        self.dir_ = dir_
        self.maximum = maximum
        self._url_manage = url_manager
        self._logger = get_logger(self.__class__.__name__)

    def run(self):
        self._logger.debug('Started running')
        # 开启url管理器
        self._url_manage.run()
        cnt = 0
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

            url = self._url_manage.new_url()
            self._logger.debug(f'New url: {url}')
            try:
                title, text = self.parse(url)
            except Exception as e:
                self._logger.error(e)
                continue
            path = f'{os.path.join(self.dir_, title)}.txt'
            # 将结果写入文档
            with open(path, 'w') as f:
                f.write(f'{text}\n')
            cnt += 1

        self._logger.debug('Done')

    @abstractmethod
    def parse(self, url) -> (str, str):
        """
        :param url: 文档url
        :return: (文档标题, 文档内容)
        """
        pass
