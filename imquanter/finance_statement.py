"""
https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
"""
from OpenDartReader.dart import OpenDartReader
from pandas import DataFrame
from pprint import pprint


class Dart(OpenDartReader):

    def func(self, symbol: str):
        """
        1분기보고서 : 11013
        반기보고서 : 11012
        3분기보고서 : 11014
        사업보고서 : 11011 (4분기)
        # "CFS":연결재무제표, "OFS":재무제표
        :param symbol:
        :return:
        """
        fs_2019 = dart.finstate_all(
            corp=symbol,
            bsns_year='2019',
            fs_div='CFS',
            reprt_code=11011)
        fs_2020_1Q = dart.finstate_all(
            corp=symbol,
            bsns_year='2020',
            fs_div='CFS',
            reprt_code=11013)

        pprint(fs_2019.to_dict(orient='index')[0])
        pprint(fs_2020_1Q.to_dict(orient='index')[0])

        equity, liability = self._get_자산총계(fs_2020_1Q)
        assets = equity + liability
        print('자산총계:', f'{assets:,}')

        profit = self._get_당기순이익(fs_2020_1Q)
        print('당기순이익:',f'{profit:,}')

        # 주식 총 발행수
        small = dart.report(symbol, '소액주주', 2020, reprt_code=11014)
        pprint(small)
        stock_tot_co = int(small['stock_tot_co'].str.replace(',', ''))
        print('주식 총 발행수:',f'{stock_tot_co:,}')

        EPS = profit / stock_tot_co
        PER = 0 / EPS
        BPS = equity / stock_tot_co
        PBR = 0 / BPS
        ROE = PBR / PER
        ROA = profit / assets

    def _get_자산총계(self, finstate):
        """자본과 부채는 재무상태표에서 당기금액('thstrm_amount') 값을 가져오면 됨"""
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
        # 2019 4분기 ~ 2020 3분기까지의 당기순이익의 합을 구하려면 2019년 4분기 당기순이익과 2020년 1분기 ~ 3분기 당기순이익의 합을 알아여함
        # 2020년 1분기 ~ 3분기 당기순이익의 합은 2020년 3분기 손익계산서에서 'thstrm_add_amount' 값을 가져오면 되고
        # 2019년 4분기 당기순이익은 2019년 전체 당기순이익에서 2019년 1분기 ~ 3분기 당기순이익의 합을 빼서 구할 수 있음

        profit = int(
            finstate.loc[
                finstate['sj_div'].isin(['IS'])
                & finstate['account_id'].isin(
                    ['ifrs-full_ProfitLossAttributableToOwnersOfParent']),
                'thstrm_add_amount' # 당기 누적 순이익
            ].replace(",", ""))
        return profit


if __name__ == '__main__':
    api_key = 'dff1bc458b903eeac7b7ea1184b7c341414f0ae3'
    samsung = '005930'

    dart = Dart(api_key=api_key)
    dart.func(samsung)