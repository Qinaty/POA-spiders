from rand_spider import Spider


if __name__ == '__main__':
    spider = Spider(
            dir_='.\\docs',
            maximum=100
    )
    spider.run()