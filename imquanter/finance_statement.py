"""
https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
"""
from OpenDartReader.dart import OpenDartReader
from pandas import DataFrame
from pprint import pprint

# 1분기보고서 : 11013
# 반기보고서 : 11012
# 3분기보고서 : 11014
# 사업보고서 : 11011 (4분기)
q2code = {
    'Q1': '11013', 'Q2': '11012',
    'Q3': '11014', 'Q4': '11011'}


class Dart(OpenDartReader):

    def get_report(self, symbol: str, year: str, quarter: str):
        """
        TODO 좀 더 다양한 재무제표 데이터 수집할 거리 생각해보기
        # "CFS":연결재무제표, "OFS":재무제표
        :param symbol: 005930
        :param year: 2022
        :param quarter: Q1,2,3,4
        :return: report(dict)
        """
        finstates = self.finstate_all(
            corp=symbol,
            bsns_year=year,
            fs_div='CFS',
            reprt_code=q2code[quarter])
        small = self.report(
            corp=symbol,
            key_word='소액주주',
            bsns_year=year)

        if finstates is not None:
            equity, liability = self._get_자산총계(finstates)
            assets = equity + liability
            profit = self._get_당기순이익(finstates)
            revenue = self._get_매출액(finstates)
            sales_flow = self._get_영업활동_현금흐름(finstates)
        else:
            equity, liability = None, None
            assets = None
            profit = None
            revenue = None
            sales_flow = None

        if small is not None:
            total_stocks = int(
                small['stock_tot_co'].str.replace(',', ''))
        else:
            total_stocks = None

        report = {
            'symbol': symbol, # 종목 코드
            'year': year, # 연도
            'quarter': quarter, # 분기
            'assets':assets, # 자산 총계
            'equity': equity, # 자본 총계
            'liability': liability, # 부채 총계
            'revenue': revenue, # 매출액
            'sales_flow': sales_flow, # 영업활동 현금흐름
            'profit': profit, # 당기 순이익
            'total_stocks': total_stocks, # 총 발행 주식수
        }
        return report

    def get_finstate_all(self, symbol: str, year: str, quarter: str):
        """재무제표 분석용 메소드"""
        finstates = self.finstate_all(
            corp=symbol,
            bsns_year=year,
            fs_div='CFS',
            reprt_code=q2code[quarter])
        return finstates.to_dict(orient='index')

    def _get_자산총계(self, finstate):
        equity = ( # 당기자본(자본총계)
            int(
                finstate.loc[
                    finstate['sj_div'].isin(['BS']) # BS : 재무상태표
                    & finstate['account_id'].isin(['ifrs-full_Equity']),
                    'thstrm_amount' # 당기 금액을 뜻 함
                ].replace(",", "")
            )
        )
        liability = ( # 당기부채(부채총계)
            int(
                finstate.loc[
                    finstate['sj_div'].isin(['BS'])
                    & finstate['account_id'].isin(
                        ['ifrs-full_Liabilities']),
                    'thstrm_amount'
                ].replace(",", "")
            )
        )
        return equity, liability

    def _get_매출액(self, finstate):
        revenue = int( # 당기 매출액
                finstate.loc[
                    finstate['sj_div'].isin(['IS'])
                    & finstate['account_id'].isin(
                        ['ifrs-full_Revenue']),
                    'thstrm_amount'
                ].replace(",", ""))
        return revenue

    def _get_당기순이익(self, finstate):
        profit = int(
            finstate.loc[
                finstate['sj_div'].isin(['IS']) # IS : 손익계산서
                & finstate['account_id'].isin(
                    ['ifrs-full_ProfitLossAttributableToOwnersOfParent']),
                'thstrm_amount'
            ].replace(",", ""))
        return profit

    def _get_영업활동_현금흐름(self, finstate):
        sales_flow = int(
            finstate.loc[
                finstate['sj_div'].isin(['CF'])
                & finstate['account_id'].isin(
                    ['ifrs-full_CashFlowsFromUsedInOperatingActivities']),
                'thstrm_amount'
            ].replace(",", ""))
        return sales_flow


if __name__ == '__main__':
    api_key = 'dff1bc458b903eeac7b7ea1184b7c341414f0ae3'
    samsung = '005930'
    year = '2021'
    quarter = 'Q2'

    dart = Dart(api_key=api_key)
    res = dart.get_finstate_all(samsung, year, quarter)
    pprint(res)