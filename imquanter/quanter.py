"""
Quanter Main Module
"""
from typing import List, Union, Optional
from pandas import DataFrame
from pprint import pprint
from tqdm import tqdm
import MySQLdb as mysql
import FinanceDataReader as fdr
from imquanter.finance_statement import Dart
from imquanter.factor_collector import FactorCollector
from imquanter.model import Price, Statement, Log, Factor
from imquanter.util import (
    get_all_kospi, log, get_quarter,
    get_quarter_sequence, now_date
)
from imquanter.query.base import Query
from imquanter.uri import URI


class Quanter:

    def __init__(self, db_uri: str, dart_api_key: str):
        self.uri = URI(uri=db_uri)
        self.db = mysql.connect(
            host=self.uri.hostname,
            port=self.uri.port,
            user=self.uri.username,
            passwd=self.uri.password,
            db=self.uri.dbname,
            charset='utf8',
            cursorclass=mysql.cursors.DictCursor,
            autocommit=True)
        self.dart = Dart(api_key=dart_api_key)
        # models
        self.price = Price(db=self.db)
        self.statement = Statement(db=self.db)
        self.log = Log(db=self.db)
        self.factor = Factor(db=self.db)

    def collect(
            self,
            start_date: Optional[str],
            end_date: Optional[str] = None,
            targets: Optional[List[str]] = None,
            symbols: Optional[List[str]] = None,
            dry: bool = False):
        """
        # 해당 종목들에 대하여, 수집할 데이터를 추출하여 DB에 저장
        :param start_date: 수집 시작 날짜
        :param end_date: 수집 마지막 날짜
        :param targets: 수집할 데이터 타입 (price, financial_statement)
        :param symbols: 수집할 종목코드 리스트
        :param dry: 테스트 실행 여부 (종목을 극소수로만 호출)
        :return: None
        """
        # Default arguments
        targets = targets if targets else ('price', 'financial_statement')
        symbols = None if symbols == 'all' else symbols
        symbols = symbols if symbols else get_all_kospi(dry=dry)

        # 타겟 종목들의 데이터를 불러와 DB에 upsert
        if 'price' in targets:
            self._collect_price(symbols, start_date, end_date)
        if 'financial_statement' in targets:
            self._collect_statement(symbols, start_date, end_date)
            self._collect_factor(symbols, start_date, end_date)
        log('# 수집 완료!')

    def get(
            self,
            filter: Optional[Query] = None,
            sort: Optional[List[tuple]] = None,
            verbose: Optional[bool] = False):
        query = f"""
        SELECT * FROM Statement s
        LEFT JOIN Factor f 
        ON 
            s.symbol = f.symbol 
            and s.`year` = f.`year` 
            and s.quarter = f.quarter
        """
        if filter:
            query += f"""
        WHERE {str(filter)}"""
        if sort:
            query += f"""
        ORDER BY {" ".join(
            [f'{i[0].lower()} {i[1].upper()}'
             for i in sort])}"""

        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        if verbose:
            log("Executed Query >")
            pprint(query)
            return DataFrame(result)
        # If Not Verbose,
        symbol_set, symbol_result = set(), []
        for i in result:
            if i['symbol'] not in symbol_set:
                symbol_set.add(i['symbol'])
                symbol_result.append(i['symbol'])
        return symbol_result

    def get_price(
            self,
            symbols: Union[str, List[str]],
            start_date: str = '0000-01-01',
            end_date: str = '9999-12-31'):
        """
        # DB에 저장된 종목 가격 정보 조회
        :param symbols: 종목 코드 리스트
        :param start_date: 시작 날짜 (Ex. 2000-01-01)
        :param end_date: 마감 날짜 (Ex. 2022-01-01)
        :return: DataFrame(
            symbol, date, Open, High, Low, Close, Volume, Change)
        """
        symbols = [symbols] if isinstance(symbols, str) else symbols
        result = self.price.search_price(
                                symbols=symbols,
                                start_date=start_date,
                                end_date=end_date)
        return DataFrame(result)


    def _collect_price(
            self,
            symbols: Union[str, List[str]],
            start_date: str,
            end_date: Optional[str] = None):
        symbols = [symbols] if isinstance(symbols, str) else symbols
        end_date = end_date if end_date else now_date()
        log('# 주가 정보 수집 개시...')
        for symbol in tqdm(symbols):
            if self.log.already_exists(
                    'collect_price',
                    symbol, start_date, end_date):
                log(f"[{symbol}]({start_date or ''}~{end_date or ''})"
                    " 주가 정보가 이미 존재하여 스킵...")
                continue
            df: DataFrame = fdr.DataReader(
                                    symbol=symbol,
                                    start=start_date,
                                    end=end_date)
            records: dict = df.to_dict(orient='index')
            for date, record in records.items():
                self.price.upsert_price({
                    'symbol': symbol,
                    'date': date.strftime('%Y-%m-%d'),
                    **record,
                })
            self.log.log_action(
                'collect_price', symbol, start_date, end_date)

    def _collect_statement(
            self,
            symbols: Union[str, List[str]],
            start_date: str,
            end_date: Optional[str] = None):
        """
        # 해당 종목들에 대하여, 수집할 데이터를 추출하여 DB에 저장
        :param symbols: 종목 코드 리스트
        :param start_date: 시작 날짜 (Ex. 2000-01-01)
        :param end_date: 마감 날짜 (Ex. 2022-01-01)
        :return: None
        """
        symbols = [symbols] if isinstance(symbols, str) else symbols
        end_date = end_date if end_date else now_date()
        sequence = get_quarter_sequence(start_date, end_date)

        log('# 재무제표 수집 개시...')
        for symbol in tqdm(symbols):
            if self.log.already_exists(
                    'collect_statement',
                    symbol, start_date, end_date):
                log(f"[{symbol}]({start_date or ''}~{end_date or ''})"
                    " 재무제표가 이미 존재하여 스킵...")
                continue
            for year, quarter in sequence:
                report = self.dart.get_report(
                                    symbol=symbol,
                                    year=year,
                                    quarter=quarter)
                if None in [*report.values()]:
                    log(
                        "정상적으로 재무제표가 수집되지 않았으므로 스킵함.->"
                        f"({symbol},{year},{quarter})")
                    continue
                self.statement.upsert_statement(report)
            self.log.log_action(
                'collect_statement', symbol, start_date, end_date)

    def _collect_factor(
            self,
            symbols: Union[str, List[str]],
            start_date: str,
            end_date: Optional[str] = None):
        """
        수집된 주가 및 재무제표 데이터를 기반으로 가치 지표 수집 및 DB에 저장
        """
        symbols = [symbols] if isinstance(symbols, str) else symbols
        end_date = end_date if end_date else now_date()
        sequence = get_quarter_sequence(start_date, end_date)

        # 팩터에 수집 최적화를 위한 데이터 Eager loading
        price_dict = {
            (i['symbol'], i['year'], i['quarter']): i['close']
            for i in self.price.get_first_quarter_price(
                            symbols, start_date, end_date)
        }
        statement_dict = {
            (i['symbol'], i['year'], i['quarter']): i
            for i in self.statement.search_statement(
                        symbols, sequence[0][0], sequence[-1][0])
        }

        log('# 가치지표 팩터 수집 개시...')
        for symbol in tqdm(symbols):
            if self.log.already_exists(
                    'collect_factor',
                    symbol, start_date, end_date):
                log(f"[{symbol}]({start_date or ''}~{end_date or ''})"
                    " 팩터 수집정보가 이미 존재하여 스킵...")
                continue
            for year, quarter in sequence:
                target = (symbol, year, quarter)
                # 주가 또는 재무제표가 수집되지 않은 종목에 대한 팩터 수집 스킵 처리
                if (target not in price_dict
                        or target not in statement_dict):
                    continue
                price = price_dict[target]
                statement = statement_dict[target]
                report = FactorCollector.collect_factor(price, statement)
                self.factor.upsert_factor(report)
            self.log.log_action(
                'collect_factor', symbol, start_date, end_date)









