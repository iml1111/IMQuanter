"""
Quanter Main Module
"""
from typing import List, Union, Optional
from pandas import DataFrame
from tinydb import TinyDB
import FinanceDataReader as fdr
from imquanter.model import Price, Statement, Log
from imquanter.util import get_all_kospi, log


class Quanter:

    def __init__(self, path='./db.json'):
        self.path = path
        self.db = TinyDB(path)
        # models
        self.price = Price(db=self.db)
        self.statement = Statement(db=self.db)
        self.log = Log(db=self.db)

    def collect(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            targets: Optional[List[str]] = None,
            symbols: Optional[List[str]] = None,
            dry: bool = True):
        """
        # 해당 종목들에 대하여, 수집할 데이터를 추출하여 DB에 저장
        :param start_date: 수집 시작 날짜
        :param end_date: 수집 마지막 날짜
        :param targets: 수집할 데이터 타입 (price, financial_statement)
        :param symbols: 수집할 종목코드 리스트
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

    def _collect_price(
            self,
            symbols: Union[str, List[str]],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        symbols = [symbols] if isinstance(symbols, str) else symbols
        for symbol in symbols:
            # 이미 수집한 적이 있을 경우, 스킵...
            if self.log.already_collect(symbol, start_date, end_date):
                log(
                    f"[{symbol}]({start_date or ''}~{end_date or ''})"
                    " 이미 수집되어 작업을 스킵합니다...")
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
                self.log.log_collect(symbol, start_date, end_date)

    def _collect_statement(
            self,
            symbols: Union[str, List[str]],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        """
        # 해당 종목들에 대하여, 수집할 데이터를 추출하여 DB에 저장
        :param symbols: 종목 코드 리스트
        :param start_date: 시작 날짜 (Ex. 2000-01-01)
        :param end_date: 마감 날짜 (Ex. 2022-01-01)
        :return: None
        """
        pass

    def get_price(
            self,
            symbols: Union[str, List[str]],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
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







