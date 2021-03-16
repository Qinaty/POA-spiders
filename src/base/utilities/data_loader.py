from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import sessionmaker

from .functions import get_logger
from .models import *


class DataLoader:
    def __init__(self, server: str, database: str):
        self._logger = get_logger(self.__class__.__name__)
        engine = create_engine(server)
        try:
            engine.execute(f'CREATE DATABASE {database}')
            self._logger.warning(f'no existing database called {database}, a new one has been created')
        except ProgrammingError:
            pass
        engine.execute(f'USE {database}')
        self._Session = sessionmaker(bind=engine)
        try:
            Base.metadata.create_all(engine)
        except OperationalError:
            pass

    def insert(self, atc: Article):
        self._logger.debug(f'trying to insert new article: {atc}')
        session = self._Session()
        session.add(atc)
        session.commit()
        self._logger.debug(f'insertion finished successfully')
