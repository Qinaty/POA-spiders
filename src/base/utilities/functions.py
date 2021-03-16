"""
工具库
"""

from random import choice
from json import load
from warnings import simplefilter
from urllib.request import getproxies
import logging

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests import get

_FORMAT = '[%(name)-10s] %(levelname)-8s: %(message)s'
_LEVEL = logging.DEBUG


def get_html(url: str) -> bytes:
    """
    解析url获得html
    :param url: 待解析URL字符串
    :return: url对应的二进制html
    """
    if not hasattr(get_html, 'ua_pool'):
        simplefilter('ignore', InsecureRequestWarning)
        with open('base\\utilities\\user_agents.json', 'r') as f:
            get_html.ua_pool = load(f)['user-agents']

    # 随机从ua_pool中取出一条user-agent
    ua = choice(get_html.ua_pool)
    # 设置请求头
    headers = {'user-agent': ua}
    # 设置代理
    proxies = getproxies()
    if 'https' in proxies.keys():
        proxies['https'] = proxies['https'].replace('s', '')
    # 获取网页内容
    html = get(url, headers=headers, proxies=proxies, verify=False).content
    return html


def letters(str_: str) -> str:
    """
    过滤字符串中的其他字符，只保留字母
    :param str_: 待过滤字符串
    :return: 过滤后的字符串
    """
    return ''.join(filter(str.isalpha, str_))


def get_logger(name) -> logging.Logger:
    """
    获取logger
    :param name: logger名称
    """
    formatter = logging.Formatter(fmt=_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(_LEVEL)
    return logger
