from abc import ABCMeta, abstractmethod
from typing import List, Union, Optional
from datetime import datetime
from MySQLdb.connections import Connection
from imquanter.util import get_quarter


class BaseModel(metaclass=ABCMeta):
    """Model Interface"""
    TABLE_QUERY = None

    def __init__(self, db: Connection):
        self._db = db
        self.table = self.__class__.__name__
        if self.TABLE_QUERY is None:
            raise NotImplementedError('TABLE QUERY가 입력되야 함.')
        self._create_table()

    def select_all(self):
        query = f'SELECT * FROM {self.table}'
        with self.mysql.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results

    def _create_table(self):
        with self._db.cursor() as cursor:
            cursor.execute(self.TABLE_QUERY % (self.table))


class Price(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(100) NOT NULL,
        `date` VARCHAR(100) NOT NULL,
        `open` BIGINT NOT NULL,
        `close` BIGINT NOT NULL,
        `high` BIGINT NOT NULL,
        `low` BIGINT NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        PRIMARY KEY (`symbol`, `date`)
    )
    """

    def upsert_price(self, document: dict):
        query = f"""
        REPLACE INTO {self.table} (
            `symbol`, `date`, `quarter`,
            `open`, `close`, `high`, `low`
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
        """
        with self._db.cursor() as cursor:
            cursor.execute(query,(
                document['symbol'],
                document['date'],
                get_quarter(document['date']),
                document['Open'],
                document['Close'],
                document['High'],
                document['Low'],
            ))

    def search_price(
            self,
            symbols: List[str],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        query = f"""
        SELECT * FROM {self.table}
        WHERE 
            `symbol` IN ({", ".join(["%s"] * len(symbols))})
            and %s <= `date` 
            and `date` <= %s 
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (*symbols, start_date, end_date))
            result = cursor.fetchall()
        return result

class Statement(BaseModel):
    TABLE_QUERY = "TODO"


class Log(BaseModel):
    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `action` VARCHAR(20) NOT NULL,
        `payload` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`action`, `payload`)
    )
    """

    def log_collect(
            self,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        query = f"""
        REPLACE INTO {self.table} (
            action, payload
        )
        VALUES (%s, %s)
        """
        payload = self.collect_payload(symbol, start_date, end_date)
        with self._db.cursor() as cursor:
            cursor.execute(query, ('collect', payload))

    def already_collect(
            self,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        payload = self.collect_payload(symbol, start_date, end_date)
        query = f"""
        SELECT * FROM {self.table}
        WHERE
            `action` = "collect"
            and `payload` = %s
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (payload,))
            result = cursor.fetchone()
        return bool(result)

    @staticmethod
    def collect_payload(symbol: str, start_date: str, end_date: str):
        return f"{symbol}_{start_date}_{end_date}"

