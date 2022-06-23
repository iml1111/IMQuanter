"""
가치 지표 수집기

# 추가 구현 목록
EV/EBITDA = (assets + net_debt) / sales_flow
EV/Sales = (assets + net_debt) / revenue
NCAV =  1 if (cur_assets - liability) > (assets * 1.5)
            and profit > 0 else 0
PEG = PER / (EPS * 100)
GP/A = gross_profit / assets
# 여러 비율
debt_ratio = liability / equity
borrow_ratio = (short_borrow + long_borrow) / equity
## 성장율 지표
revenue_growth = (revenue - pre_revenue) / pre_revenue
oper_income_growth = (oper_income - pre_oper_income) / pre_oper_income
## 회전율 지표
asset_turnover = revenue / assets
trade_receive_turnover = revenue / trade_receive
inventory_turnover = cost_sales / inventories
## 이익률 지표
gross_margin = gross_profit / revenue
oper_margin = oper_income / revenue
profit_margin = profit / revenue

# 쿼리로 구현해야 할듯
RIM = assets + (assets * roe - X) / X)
"""


class FactorCollector:

    def collect_factor(self, price: int, statement: dict):
        """
        추가로 수집할 가치 지표를 이곳에서 작성하세요.
        price: 해당 분기의 첫 종가(Close Price)
        statement: 해당 분기의 재무제표
        """
        s = statement
        dv = self.div_without_zero

        EPS = dv(s['profit'], s['total_stocks'])
        PER = dv(price, EPS)
        BPS = dv(s['equity'], statement['total_stocks'])
        PBR = dv(price, BPS)
        SPS = dv(s['revenue'], s['total_stocks'])
        PSR = dv(price, SPS)
        CPS = dv(s['sales_flow'], s['total_stocks'])
        PCR = dv(price, CPS)
        combo_4 = self.가치투자_4대장_콤보(PER, PBR, PCR, PSR)
        ROE = dv(PBR, PER)
        ROA = dv(s['profit'], s['assets'])
        EV_EVITDA = dv(s['assets'] + s['net_debt'], s['sales_flow'])
        EV_Salse = dv(s['assets'] + s['net_debt'], s['revenue'])
        NCAV = self.NCAV(s)
        PEG = dv(PER, (EPS * 100))
        GP_A = dv(s['gross_profit'], s['assets'])
        # 부채비율
        debt_ratio = dv(s['liability'], s['equity'])
        # 차입금비율
        borrow_ratio = dv((s['short_borrow'] + s['long_borrow']), s['equity'])
        # 성장률지표
        revenue_growth = dv((s['revenue'] - s['pre_revenue']), s['pre_revenue'])
        oper_income_growth = dv(
            (s['oper_income'] - s['pre_oper_income']), s['pre_oper_income'])
        # 회전율지표
        asset_turnover = dv(s['revenue'], s['assets'])
        trade_receive_turnover = dv(s['revenue'], s['trade_receive'])
        inventory_turnover = dv(s['cost_sales'], s['inventories'])
        # 이익률지표
        gross_margin = dv(s['gross_profit'], s['revenue'])
        oper_margin = dv(s['oper_income'], s['revenue'])
        profit_margin = dv(s['profit'], s['revenue'])

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
            'ev_evitda': EV_EVITDA,
            'ev_sales': EV_Salse,
            'ncav': NCAV,
            'peg': PEG,
            'gp_a': GP_A,
            'debt_ratio': debt_ratio,
            'borrow_ratio': borrow_ratio,
            'revenue_growth': revenue_growth,
            'oper_income_growth': oper_income_growth,
            'asset_turnover': asset_turnover,
            'trade_receive_turnover': trade_receive_turnover,
            'inventory_turnover': inventory_turnover,
            'gross_margin': gross_margin,
            'oper_margin': oper_margin,
            'profit_margin': profit_margin,
        }

    @staticmethod
    def 가치투자_4대장_콤보(*args):
        return sum(args)

    @staticmethod
    def NCAV(s):
        if (
            (s['cur_assets'] - s['liability']) > (s['assets'] * 1.5)
            and s['profit'] > 0
        ):
            return 1
        else:
            return 0

    @staticmethod
    def div_without_zero(a, b):
        if b != 0:
            return a / b
        else:
            return 0
