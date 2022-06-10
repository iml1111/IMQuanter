"""

"""
from .base import BaseModel


class Statement(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(20) NOT NULL,
        `year` VARCHAR(10) NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        `assets` BIGINT NOT NULL,
        `equity` BIGINT NOT NULL,
        `liability` BIGINT NOT NULL,
        `profit` BIGINT NOT NULL,
        `total_stocks` BIGINT,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """

    def upsert_statement(self, document: dict):
        query = f"""
        REPLACE INTO {self.table} (
            `symbol`, `year`, `quarter`,
            `assets`, `equity`, `liability`, `profit`,
            `total_stocks`
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (
                document['symbol'],
                document['year'],
                document['quarter'],
                document['assets'],
                document['equity'],
                document['liability'],
                document['profit'],
                document['total_stocks'],
            ))