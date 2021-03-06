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
        `pre_revenue` BIGINT,
        `sales_flow` BIGINT,
        `profit` BIGINT,
        `total_stocks` BIGINT,
        `net_debt` BIGINT,
        `cur_assets` BIGINT,
        `gross_profit` BIGINT,
        `short_borrow` BIGINT,
        `long_borrow` BIGINT,
        `pre_oper_income` BIGINT,
        `oper_income` BIGINT,
        `trade_receive` BIGINT,
        `inventories` BIGINT,
        `cost_sales` BIGINT,
        `g_assets` BIGINT,
        `g_comprehensiveincome` BIGINT,
        `g_costofsales` BIGINT,
        `g_currentassets` BIGINT,
        `g_currentliabilities` BIGINT,
        `g_currentprovisions` BIGINT,
        `g_deferredtaxassets` BIGINT,
        `g_dividendspaid` BIGINT,
        `g_equity` BIGINT,
        `g_financeincome` BIGINT,
        `g_grossprofit` BIGINT,
        `g_inventories` BIGINT,
        `g_issuedcapital` BIGINT,
        `g_liabilities` BIGINT,
        `g_noncurrentassets` BIGINT,
        `g_profitloss` BIGINT,
        `g_profitlossbeforetax` BIGINT,
        `g_retainedearnings` BIGINT,
        `g_revenue` BIGINT,
        `g_sharepremium` BIGINT,
        `g_shorttermborrowings` BIGINT,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """

    def upsert_statement(self, document: dict):
        query = f"""
        INSERT INTO {self.table} (
            `symbol`, `year`, `quarter`,
            `assets`, `equity`, `liability`, 
            `revenue`, `pre_revenue`, `sales_flow`, `profit`, 
            `total_stocks`,
            `net_debt`,
            `cur_assets`,
            `gross_profit`,
            `short_borrow`,
            `long_borrow`,
            `pre_oper_income`,
            `oper_income`,
            `trade_receive`,
            `inventories`,
            `cost_sales`,
            `g_assets`,
            `g_comprehensiveincome`,
            `g_costofsales`,
            `g_currentassets`,
            `g_currentliabilities`,
            `g_currentprovisions`,
            `g_deferredtaxassets`,
            `g_dividendspaid`,
            `g_equity`,
            `g_financeincome`,
            `g_grossprofit`,
            `g_inventories`,
            `g_issuedcapital`,
            `g_liabilities`,
            `g_noncurrentassets`,
            `g_profitloss`,
            `g_profitlossbeforetax`,
            `g_retainedearnings`,
            `g_revenue`,
            `g_sharepremium`,
            `g_shorttermborrowings`
        )
        VALUES ({", ".join(["%s"] * 42)}) 
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
                document['pre_revenue'],
                document['sales_flow'],
                document['profit'],
                document['total_stocks'],
                document['net_debt'],
                document['cur_assets'],
                document['gross_profit'],
                document['short_borrow'],
                document['long_borrow'],
                document['pre_oper_income'],
                document['oper_income'],
                document['trade_receive'],
                document['inventories'],
                document['cost_sales'],
                document.get('g_assets'),
                document.get('g_comprehensiveincome'),
                document.get('g_costofsales'),
                document.get('g_currentassets'),
                document.get('g_currentliabilities'),
                document.get('g_currentprovisions'),
                document.get('g_deferredtaxassets'),
                document.get('g_dividendspaid'),
                document.get('g_equity'),
                document.get('g_financeincome'),
                document.get('g_grossprofit'),
                document.get('g_inventories'),
                document.get('g_issuedcapital'),
                document.get('g_liabilities'),
                document.get('g_noncurrentassets'),
                document.get('g_profitloss'),
                document.get('g_profitlossbeforetax'),
                document.get('g_retainedearnings'),
                document.get('g_revenue'),
                document.get('g_sharepremium'),
                document.get('g_shorttermborrowings'),
            ))

    def insert_statements(self, documents: dict):
        query = f"""
        REPLACE INTO {self.table} (
            `symbol`, `year`, `quarter`,
            `assets`, `equity`, `liability`, 
            `revenue`, `pre_revenue`, `sales_flow`, `profit`, 
            `total_stocks`,
            `net_debt`,
            `cur_assets`,
            `gross_profit`,
            `short_borrow`,
            `long_borrow`,
            `pre_oper_income`,
            `oper_income`,
            `trade_receive`,
            `inventories`,
            `cost_sales`,
            `g_assets`,
            `g_comprehensiveincome`,
            `g_costofsales`,
            `g_currentassets`,
            `g_currentliabilities`,
            `g_currentprovisions`,
            `g_deferredtaxassets`,
            `g_dividendspaid`,
            `g_equity`,
            `g_financeincome`,
            `g_grossprofit`,
            `g_inventories`,
            `g_issuedcapital`,
            `g_liabilities`,
            `g_noncurrentassets`,
            `g_profitloss`,
            `g_profitlossbeforetax`,
            `g_retainedearnings`,
            `g_revenue`,
            `g_sharepremium`,
            `g_shorttermborrowings`
        )
        VALUES ({", ".join(["%s"] * 42)}) 
        """
        rows = []
        for document in documents:
            rows.append((
                document['symbol'],
                document['year'],
                document['quarter'],
                document['assets'],
                document['equity'],
                document['liability'],
                document['revenue'],
                document['pre_revenue'],
                document['sales_flow'],
                document['profit'],
                document['total_stocks'],
                document['net_debt'],
                document['cur_assets'],
                document['gross_profit'],
                document['short_borrow'],
                document['long_borrow'],
                document['pre_oper_income'],
                document['oper_income'],
                document['trade_receive'],
                document['inventories'],
                document['cost_sales'],
                document['g_assets'],
                document['g_comprehensiveincome'],
                document['g_costofsales'],
                document['g_currentassets'],
                document['g_currentliabilities'],
                document['g_currentprovisions'],
                document['g_deferredtaxassets'],
                document['g_dividendspaid'],
                document['g_equity'],
                document['g_financeincome'],
                document['g_grossprofit'],
                document['g_inventories'],
                document['g_issuedcapital'],
                document['g_liabilities'],
                document['g_noncurrentassets'],
                document['g_profitloss'],
                document['g_profitlossbeforetax'],
                document['g_retainedearnings'],
                document['g_revenue'],
                document['g_sharepremium'],
                document['g_shorttermborrowings'],
            ))
        with self._db.cursor() as cursor:
            cursor.executemany(query, rows)

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