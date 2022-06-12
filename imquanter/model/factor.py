"""
가치 지표 수집 테이블
"""
from .base import BaseModel


class Factor(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(20) NOT NULL,
        `year` VARCHAR(10) NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        `eps` DOUBLE,
        `per` DOUBLE,
        `bps` DOUBLE,
        `pbr` DOUBLE,
        `roe` DOUBLE,
        `roa` DOUBLE,
        `sps` DOUBLE,
        `psr` DOUBLE,
        `cps` DOUBLE,
        `pcr` DOUBLE,
        `combo_4` DOUBLE,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """

    def upsert_factor(self, document: dict):
        query = f"""
        REPLACE INTO {self.table} (
            `symbol`, `year`, `quarter`,
            `eps`,
            `per`,
            `bps`,
            `pbr`,
            `roe`,
            `roa`,
            `sps`,
            `psr`,
            `cps`,
            `pcr`,
            `combo_4`
        )
        VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        ) 
        """
        with self._db.cursor() as cursor:
            cursor.execute(query,(
                document['symbol'],
                document['year'],
                document['quarter'],
                document['eps'],
                document['per'],
                document['bps'],
                document['pbr'],
                document['roe'],
                document['roa'],
                document['sps'],
                document['psr'],
                document['cps'],
                document['pcr'],
                document['combo_4'],
            ))