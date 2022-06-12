"""
가치 지표 수집기
# EPS = profit / total_stocks
# PER = price / EPS
# BPS = equity / total_stocks
# PBR = price / BPS
# ROE = PBR / PER
# ROA = profit / assets
# SPS = revenue / total_stocks
# PSR = price / SPS
"""


class FactorCollector:

    @staticmethod
    def collect_factor(price: int, statement: dict):
        EPS = statement['profit'] / statement['total_stocks']
        PER = price / EPS
        BPS = statement['equity'] / statement['total_stocks']
        PBR = price / BPS
        SPS = statement['revenue'] / statement['total_stocks']
        PSR = price / SPS
        CPS = statement['sales_flow'] / statement['total_stocks']
        PCR = price / CPS

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
        }
