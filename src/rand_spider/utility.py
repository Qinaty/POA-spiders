"""
工具库
"""
from random import choice
from json import load
from requests import get
import logging

# 配置日志格式和显示等级，仅在本模块内使用，外部不可见
_FORMAT = '[%(name)-10s] %(levelname)-8s %(message)s'
_LEVEL = logging.DEBUG


def get_logger(name: str):
    """
    :param name: 日志记录器的名字
    :return: 以name命名的日志记录器
    """
    formatter = logging.Formatter(fmt=_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(_LEVEL)
    return logger


def get_html(url: str) -> bytes:
    """
    解析url获得html
    :param url: 待解析URL字符串
    :return: url对应的二进制html
    """
    # 如果是第一次调用，需要读取User-Agents列表到ua_pool中
    if not hasattr(get_html, 'ua_pool'):
        with open('rand_spider\\user_agents.json', 'r') as f:
            get_html.ua_pool = load(f)['user-agents']

    ua = choice(get_html.ua_pool)  # 随机从ua_pool中取出一条user-agent
    headers = {'user-agent': ua}
    html = get(url, headers=headers).content
    return html


def letters(str_: str):
    """
    过滤字符串中的其他字符，只保留字母
    :param str_: 待过滤字符串
    :return: 过滤后的字符串
    """
    return ''.join(filter(str.isalpha, str_))
