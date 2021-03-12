from base import *
from datetime import date

USER = 'root'
PASSWORD = 'sy100109'
HOST = 'localhost'
PORT = '3306'

atc = Article(
    publisher='azhe',
    url='www.azhe.com',
    title='啊这',
    date=date(2021, 2, 3).strftime('%Y-%m-%d'),
    author='阿哲',
    content='啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这啊这',
    abstract='啊这啊这啊这',
    location='Azherica',
    section='啊这',
    category='啊这',
    pic_url='www.azhepic.com',
    type='media'
)

dl = DataLoader(
    server=f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}',
    database='test_db'
)

dl.insert(atc)
