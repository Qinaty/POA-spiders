"""
工具库
"""

from random import choice
from json import load
from requests import get


def get_html(url: str) -> bytes:
    """
    解析url获得html
    :param url: 待解析URL字符串
    :return: url对应的二进制html
    """
    # 如果是第一次调用，需要读取User-Agents列表到ua_pool中
    if not hasattr(get_html, 'ua_pool'):
        with open('base\\utilities\\user_agents.json', 'r') as f:
            get_html.ua_pool = load(f)['user-agents']

    # 随机从ua_pool中取出一条user-agent
    ua = choice(get_html.ua_pool)
    headers = {'user-agent': ua}
    html = get(url, headers=headers).content
    return html


def letters(str_: str) -> str:
    """
    过滤字符串中的其他字符，只保留字母
    :param str_: 待过滤字符串
    :return: 过滤后的字符串
    """
    return ''.join(filter(str.isalpha, str_))
