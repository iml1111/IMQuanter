"""
수정 주가 수집 테이블
"""
from .base import BaseModel
from typing import List, Optional
from imquanter.util import get_quarter


class Price(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(20) NOT NULL,
        `date` VARCHAR(20) NOT NULL,
        `open` BIGINT NOT NULL,
        `close` BIGINT NOT NULL,
        `high` BIGINT NOT NULL,
        `low` BIGINT NOT NULL,
        `year` VARCHAR(10) NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        PRIMARY KEY (`symbol`, `date`)
    )
    """

    def insert_prices(self, documents: list):
        rows = []
        for document in documents:
            rows.append((
                document['symbol'],
                document['date'],
                document['date'][:4],
                get_quarter(document['date']),
                document['Open'],
                document['Close'],
                document['High'],
                document['Low'],
            ))
        query = f"""
        INSERT INTO {self.table} (
            `symbol`, `date`, `year`, `quarter`,
            `open`, `close`, `high`, `low`
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
        """
        with self._db.cursor() as cursor:
            cursor.executemany(query, rows)


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

    def get_first_quarter_price(
            self,
            symbols: List[str],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        query = f"""
        SELECT a.symbol, a.year, a.quarter, b.close 
        FROM (
            SELECT 
            symbol, year, quarter, 
            MIN(date) as min_date
            FROM {self.table}
            WHERE
                `symbol` IN ({", ".join(["%s"] * len(symbols))})
                and %s <= date 
                and date <= %s	
            GROUP BY symbol, year, quarter 
        ) a
        LEFT JOIN {self.table} b
        ON a.symbol=b.symbol AND a.min_date=b.date
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (*symbols, start_date, end_date))
            result = cursor.fetchall()
        return result
