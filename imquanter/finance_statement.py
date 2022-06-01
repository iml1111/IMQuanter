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
        else:
            equity, liability = None, None
            assets = None
            profit = None

        if small:
            total_stocks = int(
                small['stock_tot_co'].str.replace(',', ''))
        else:
            total_stocks = None

        report = {
            'symbol': symbol,
            'year': year,
            'quarter': quarter,
            'assets':assets, # 자산 총계
            'equity': equity, # 자본 총계
            'liability': liability, # 부채 총계
            'profit': profit, # 당기 순이익
            'total_stocks': total_stocks, # 총 발행 주식수
        }
        return report
        # TODO 가치지표 따로 측정하기
        # EPS = profit / stock_tot_co
        # PER = 0 / EPS
        # BPS = equity / stock_tot_co
        # PBR = 0 / BPS
        # ROE = PBR / PER
        # ROA = profit / assets

    def _get_자산총계(self, finstate):
        """
        BS : 재무상태표
        자본과 부채는 재무상태표에서 당기금액('thstrm_amount') 값을 가져오면 됨
        """
        equity = ( # 당기자본(자본총계)
            int(
                finstate.loc[
                    finstate['sj_div'].isin(['BS'])
                    & finstate['account_id'].isin(['ifrs-full_Equity']),
                    'thstrm_amount'
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

    def _get_당기순이익(self, finstate):
        """
         IS : 손익계산서
        """
        profit = int(
            finstate.loc[
                finstate['sj_div'].isin(['IS'])
                & finstate['account_id'].isin(
                    ['ifrs-full_ProfitLossAttributableToOwnersOfParent']),
                'thstrm_amount' # 당기 순이익
            ].replace(",", ""))
        return profit


if __name__ == '__main__':
    api_key = 'dff1bc458b903eeac7b7ea1184b7c341414f0ae3'
    samsung = '005930'
    year = '2022'
    quarter = 'Q1'

    dart = Dart(api_key=api_key)
    res = dart.get_report(samsung, year, quarter)
    pprint(res)