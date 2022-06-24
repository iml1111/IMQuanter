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
        `ev_evitda` DOUBLE,
        `ev_sales` DOUBLE,
        `ncav` DOUBLE,
        `peg` DOUBLE,
        `gp_a` DOUBLE,
        `debt_ratio` DOUBLE,
        `borrow_ratio` DOUBLE,
        `revenue_growth` DOUBLE,
        `oper_income_growth` DOUBLE,
        `asset_turnover` DOUBLE,
        `trade_receive_turnover` DOUBLE,
        `inventory_turnover` DOUBLE,
        `gross_margin` DOUBLE,
        `oper_margin` DOUBLE,
        `profit_margin` DOUBLE,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """

    def insert_factors(self, documents: list):
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
            `combo_4`,
            `ev_evitda`,
            `ev_sales`,
            `ncav`,
            `peg`,
            `gp_a`,
            `debt_ratio`,
            `borrow_ratio`,
            `revenue_growth`,
            `oper_income_growth`,
            `asset_turnover`,
            `trade_receive_turnover`,
            `inventory_turnover`,
            `gross_margin`,
            `oper_margin`,
            `profit_margin`
        )
        VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        ) 
        """
        rows = []
        for document in documents:
            rows.append((
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
                document['ev_evitda'],
                document['ev_sales'],
                document['ncav'],
                document['peg'],
                document['gp_a'],
                document['debt_ratio'],
                document['borrow_ratio'],
                document['revenue_growth'],
                document['oper_income_growth'],
                document['asset_turnover'],
                document['trade_receive_turnover'],
                document['inventory_turnover'],
                document['gross_margin'],
                document['oper_margin'],
                document['profit_margin'],
            ))
        with self._db.cursor() as cursor:
            cursor.executemany(query, rows)