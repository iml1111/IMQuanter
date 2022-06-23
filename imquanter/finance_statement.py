"""
https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
"""
import time

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

    def get_report(
            self,
            symbol: str,
            year: str,
            quarter: str,
            include_general: bool = False):
        """
        # "CFS":연결재무제표, "OFS":재무제표
        :param symbol: 005930
        :param year: 2022
        :param quarter: Q1,2,3,4
        :param include_general: 기타 데이터 포함여부
        :return: report(dict)
        """
        finstates = self.finstate_all(
            corp=symbol,
            bsns_year=year,
            fs_div='CFS',
            reprt_code=q2code[quarter])
        time.sleep(1)
        small = self.report(
            corp=symbol,
            key_word='소액주주',
            bsns_year=year)

        if finstates is not None:
            equity, liability = self._get_자산총계(finstates)
            assets = equity + liability
            profit = self._get_당기순이익(finstates)
            revenue = self._get_매출액(finstates)
            pre_revenue = self._get_전기_매출액(finstates)
            oper_incomes = self._get_영업이익(finstates)
            sales_flow = self._get_영업활동_현금흐름(finstates)
            net_debt = self._get_순차입금(finstates)
            cur_assets = self._get_유동자산(finstates)
            gross_profit = self._get_매출총이익(finstates)
            short_borrow, long_borrow = (
                self._get_장단기차입금(finstates))
            trade_receive = self._get_매출채권(finstates)
            inventories = self._get_재고자산(finstates)
            cost_sales = self._get_매출원가(finstates)

            if include_general:
                general_data = self.get_general_data(finstates)
            else:
                general_data = {}
        else:
            return {'fail': None}

        if small is not None:
            total_stocks = int(
                small['stock_tot_co'].str.replace(',', ''))
        else:
            return {'fail': None}

        return {
            'symbol': symbol, # 종목 코드
            'year': year, # 연도
            'quarter': quarter, # 분기
            'assets':assets, # 자산 총계
            'equity': equity, # 자본 총계
            'liability': liability, # 부채 총계
            'revenue': revenue, # 매출액
            'pre_revenue': pre_revenue, # 전기 매출액
            'sales_flow': sales_flow, # 영업활동 현금흐름, EBITDA
            'profit': profit, # 당기 순이익
            'total_stocks': total_stocks, # 총 발행 주식수
            'net_debt': net_debt, # 순차입금
            'cur_assets': cur_assets, # 유동자산
            'gross_profit': gross_profit, # 매출 총이익
            'short_borrow': short_borrow, # 단기차입금
            'long_borrow': long_borrow, # 장기차입금
            'pre_oper_income': oper_incomes[0], # 전기 영업이익
            'oper_income': oper_incomes[1], # 당기 영업이익
            'trade_receive': trade_receive, # 매출채권
            'inventories': inventories, # 재고자산
            'cost_sales': cost_sales, # 매출원가
            **general_data, # 그 외 나머지 데이터들
        }

    def get_finstate_all(self, symbol: str, year: str, quarter: str):
        """재무제표 분석용 메소드"""
        finstates = self.finstate_all(
            corp=symbol,
            bsns_year=year,
            fs_div='CFS',
            reprt_code=q2code[quarter])
        return finstates.to_dict(orient='index')
        #return finstates

    def get_general_data(self, finstates):
        """그외의 재무제표 데이터를 일단 수집"""
        dicts = finstates.to_dict(orient='index')
        result = []
        for value in dicts.values():
            acc_id = value['account_id']
            if (isinstance(acc_id, str)
                    and acc_id.startswith('ifrs-full')
                    and len(acc_id) < 30):
                conv_id = self._convert_acc_id(acc_id)
                amount = value['thstrm_amount']
                result.append((conv_id, amount))
        return {i[0]:i[1] for i in result[::-1]}

    def _convert_acc_id(self, acc_id: str):
        acc_id = acc_id.replace('ifrs-full_', '')
        acc_id = acc_id.lower()
        return "g_" + acc_id

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

    def _get_전기_매출액(self, finstate):
        try:
            return int( # 전기 매출액
                    finstate.loc[
                        finstate['sj_div'].isin(['IS'])
                        & finstate['account_id'].isin(
                            ['ifrs-full_Revenue']),
                        'frmtrm_amount'
                    ].replace(",", ""))
        except ValueError:
            return int(  # 전기 매출액
                finstate.loc[
                    finstate['sj_div'].isin(['IS'])
                    & finstate['account_id'].isin(
                        ['ifrs-full_Revenue']),
                    'frmtrm_q_amount'
                ].replace(",", ""))

    def _get_매출총이익(self, finstate):
        revenue = int( # 당기 매출 총이익
                finstate.loc[
                    finstate['sj_div'].isin(['IS'])
                    & finstate['account_id'].isin(
                        ['ifrs-full_GrossProfit']),
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

    def _get_순차입금(self, finstate):
        순차입금 = finstate.loc[
                finstate['sj_div'].isin(['CF'])
                & finstate['account_nm'].isin(
                    ['단기차입금의 순증가(감소)']),
                'thstrm_amount'
            ].replace(",", "")
        if isinstance(순차입금, str):
            return int(순차입금) * (-1)
        else:
            return 0

    def _get_유동자산(self, finstate):
        a = finstate.loc[
                finstate['sj_div'].isin(['CF'])
                & finstate['account_id'].isin(
                    ['ifrs-full_CurrentAssets']),
                'thstrm_amount'
            ].replace(",", "")
        if isinstance(a, str):
            return int(a)
        else:
            return 0

    def _get_장단기차입금(self, finstate):
        단기차입금 = int(
            finstate.loc[
                finstate['sj_div'].isin(['BS'])
                & finstate['account_id'].isin(
                    ['ifrs-full_ShorttermBorrowings']),
                'thstrm_amount'
            ].replace(",", ""))
        장기차입금 = int(
            finstate.loc[
                finstate['sj_div'].isin(['BS'])
                & finstate['account_id'].isin(
                    ['dart_LongTermBorrowingsGross']),
                'thstrm_amount'
            ].replace(",", ""))
        return 단기차입금, 장기차입금

    def _get_영업이익(self, finstate):
        try:
            전기_영업이익 = int(
                finstate.loc[
                    finstate['sj_div'].isin(['IS'])
                    & finstate['account_id'].isin(
                        ['dart_OperatingIncomeLoss']),
                    'frmtrm_amount'
                ].replace(",", ""))
        except ValueError:
            전기_영업이익 = int(
                finstate.loc[
                    finstate['sj_div'].isin(['IS'])
                    & finstate['account_id'].isin(
                        ['dart_OperatingIncomeLoss']),
                    'frmtrm_q_amount'
                ].replace(",", ""))
        당기_영업이익 = int(
            finstate.loc[
                finstate['sj_div'].isin(['IS'])
                & finstate['account_id'].isin(
                    ['dart_OperatingIncomeLoss']),
                'thstrm_amount'
            ].replace(",", ""))
        return 전기_영업이익, 당기_영업이익

    def _get_매출채권(self, finstate):
        return int(
            finstate.loc[
                finstate['sj_div'].isin(['BS'])
                & finstate['account_id'].isin(
                    ['dart_ShortTermTradeReceivable']),
                'thstrm_amount'
            ].replace(",", ""))

    def _get_매출원가(self, finstate):
        return int(
            finstate.loc[
                finstate['sj_div'].isin(['IS'])
                & finstate['account_id'].isin(
                    ['ifrs-full_CostOfSales']),
                'thstrm_amount'
            ].replace(",", ""))

    def _get_재고자산(self, finstate):
        a = finstate.loc[
                finstate['sj_div'].isin(['IS'])
                & finstate['account_id'].isin(
                    ['ifrs-full_Inventories']),
                'thstrm_amount'
            ].replace(",", "")
        if isinstance(a, str):
            return int(a)
        else:
            return 0


if __name__ == '__main__':
    api_key = 'dff1bc458b903eeac7b7ea1184b7c341414f0ae3'
    samsung = '005930'
    year = '2020'
    quarter = 'Q1'

    dart = Dart(api_key=api_key)
    res = dart.get_finstate_all(samsung, year, quarter)
    pprint(res)
