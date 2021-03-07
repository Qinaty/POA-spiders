import os

from Rand import *
from CNN import *


def test_rand():
    try:
        os.mkdir('./rand_docs')
    except FileExistsError:
        pass
    url_manager = RandURLManager()
    spider = RandSpider(dir_='./rand_docs', url_manager=url_manager, maximum=10)
    spider.run()


def test_cnn():
    try:
        os.mkdir('./cnn_docs')
    except FileExistsError:
        pass
    url_manager = CNNURLManager()
    spider = CNNSpider(dir_='./cnn_docs', url_manager=url_manager, maximum=10)
    spider.run()


if __name__ == '__main__':
    # test_rand()
    test_cnn()
