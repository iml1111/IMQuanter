from abc import ABCMeta
from typing import List, Union, Optional
from tinydb import TinyDB, Query
from datetime import datetime


class BaseModel(metaclass=ABCMeta):
    """
    Model Interface
    # https://tinydb.readthedocs.io/en/latest/api.html#tinydb-table
    """

    def __init__(self, db: TinyDB):
        self._db = db
        self._table = db.table(self.__class__.__name__)

    def insert_one(self, document: dict):
        self._table.insert(
            document=self._schemize(document))

    def upsert_one(self, document: dict, condition):
        self._table.upsert(
            document=self._schemize(document),
            cond=condition)

    def insert_many(self, documents: list):
        documents = [self._schemize(i) for i in documents]
        self._table.insert_multiple(documents=documents)

    def _schemize(self, document: dict):
        return {
            'updated_at': datetime.now().strftime('%Y-%m-%d'),
            **document,
        }


class Price(BaseModel):

    def upsert_price(self, document: dict):
        Q = Query()
        self.upsert_one(
            document=document,
            condition=(
                (Q.symbol == document['symbol'])
                & (Q.date == document['date'])
            )
        )

    def search_price(
            self,
            symbols: List[str],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        Q = Query()
        results = self._table.search(
            Q.symbol.one_of(symbols)
            & (Q.date >= start_date if start_date else Q.noop())
            & (Q.date <= end_date if end_date else Q.noop())
        )
        for i in results:
            del i['updated_at']
        return results


class Statement(BaseModel):
    pass


class Log(BaseModel):

    def log_collect(
            self,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        self.insert_one({
            'action': 'collect',
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date
        })

    def already_collect(
            self,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        Q = Query()
        result = self._table.search(
            (Q.action == 'collect')
            & (Q.symbol == symbol)
            & (Q.start_date == start_date)
            & (Q.end_date == end_date))
        return bool(result)

