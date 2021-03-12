from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .utilities import get_logger
from .models import *


class DataLoader:
    def __init__(self, database_url: str):
        engine = create_engine(database_url, echo=True)
        self._logger = get_logger(self.__class__.__name__)
        self._Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

    def insert(self, atc: Article):
        session = self._Session()
        session.add(atc)
        session.commit()
