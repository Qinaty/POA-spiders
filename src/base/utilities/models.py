from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, DATE, ENUM

Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'

    id = Column(INTEGER, primary_key=True)
    publisher = Column(VARCHAR(16), nullable=False)
    url = Column(TEXT, nullable=False)
    title = Column(VARCHAR(256), nullable=False)
    date = Column(DATE, nullable=False)
    content = Column(TEXT, nullable=False)
    authors = Column(TEXT)
    abstract = Column(TEXT)
    location = Column(VARCHAR(32))
    section = Column(VARCHAR(32))
    category = Column(VARCHAR(32))
    pic_url = Column(TEXT)
    type = Column(
        ENUM(
            'media',
            'passage',
            'event'
        ),
        nullable=False,
    )

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}')>"
