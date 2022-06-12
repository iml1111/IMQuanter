"""

"""
from typing import List, Optional, Union
from .base import BaseModel


class Statement(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(20) NOT NULL,
        `year` VARCHAR(10) NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        `assets` BIGINT,
        `equity` BIGINT,
        `liability` BIGINT,
        `revenue` BIGINT,
        `sales_flow` BIGINT,
        `profit` BIGINT,
        `total_stocks` BIGINT,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """

    def upsert_statement(self, document: dict):
        query = f"""
        REPLACE INTO {self.table} (
            `symbol`, `year`, `quarter`,
            `assets`, `equity`, `liability`, 
            `revenue`, `sales_flow`, `profit`, 
            `total_stocks`
        )
        VALUES (
            %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, 
            %s
        ) 
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (
                document['symbol'],
                document['year'],
                document['quarter'],
                document['assets'],
                document['equity'],
                document['liability'],
                document['revenue'],
                document['sales_flow'],
                document['profit'],
                document['total_stocks'],
            ))

    def search_statement(
            self,
            symbols: List[str],
            start_year: Optional[str] = None,
            end_year: Optional[str] = None):
        query = f"""
        SELECT * FROM {self.table}
        WHERE
            `symbol` IN ({", ".join(["%s"] * len(symbols))})
            and %s <= year 
            and year <= %s
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (*symbols, start_year, end_year))
            result = cursor.fetchall()
        return result