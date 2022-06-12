"""
가치 지표 수집기
"""


class FactorCollector:

    def collect_factor(self, price: int, statement: dict):
        """
        추가로 수집할 가치 지표를 이곳에서 작성하세요.
        price: 해당 분기의 첫 종가(Close Price)
        statement: 해당 분기의 재무제표
        """
        EPS = statement['profit'] / statement['total_stocks']
        PER = price / EPS
        BPS = statement['equity'] / statement['total_stocks']
        PBR = price / BPS
        SPS = statement['revenue'] / statement['total_stocks']
        PSR = price / SPS
        CPS = statement['sales_flow'] / statement['total_stocks']
        PCR = price / CPS
        combo_4 = self.가치투자_4대장_콤보(PER, PBR, PCR, PSR)

        return {
            'symbol': statement['symbol'],
            'year': statement['year'],
            'quarter': statement['quarter'],
            'eps': EPS,
            'per': PER,
            'bps': BPS,
            'pbr': PBR,
            'roe': PBR / PER,
            'roa': statement['profit'] / statement['assets'],
            'sps': SPS,
            'psr': PSR,
            'cps': CPS,
            'pcr': PCR,
            'combo_4': combo_4,
        }

    @staticmethod
    def 가치투자_4대장_콤보(*args):
        return sum(args)
