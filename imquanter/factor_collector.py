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
        if EPS > 0:
            PER = price / EPS
        else:
            PER = 0
        BPS = statement['equity'] / statement['total_stocks']
        if BPS > 0:
            PBR = price / BPS
        else:
            PBR = 0
        SPS = statement['revenue'] / statement['total_stocks']
        if SPS > 0:
            PSR = price / SPS
        else:
            PSR = 0
        CPS = statement['sales_flow'] / statement['total_stocks']
        if CPS > 0:
            PCR = price / CPS
        else:
            PCR = 0
        combo_4 = self.가치투자_4대장_콤보(PER, PBR, PCR, PSR)

        if PER > 0:
            ROE = PBR / PER
        else:
            ROE = 0

        if statement['assets'] != 0:
            ROA = statement['profit'] / statement['assets']
        else:
            ROA = 0

        return {
            'symbol': statement['symbol'],
            'year': statement['year'],
            'quarter': statement['quarter'],
            'eps': EPS,
            'per': PER,
            'bps': BPS,
            'pbr': PBR,
            'roe': ROE,
            'roa': ROA,
            'sps': SPS,
            'psr': PSR,
            'cps': CPS,
            'pcr': PCR,
            'combo_4': combo_4,
        }

    @staticmethod
    def 가치투자_4대장_콤보(*args):
        return sum(args)
