from imquanter.query.base import Factor
from imquanter.util import type_valid


class Metric(Factor):
    METRIC = None

    def __init__(
            self,
            gte: float = None,
            lte: float = None):
        self.gte = gte
        self.lte = lte

    @property
    def query(self):
        strings = []
        if self.gte is not None:
            strings.append(f"{self.gte} <= {self.METRIC}")
        if self.lte is not None:
            strings.append(f"{self.METRIC} <= {self.lte}")
        return f'({" AND ".join(strings)})'


class EPS(Metric):
    METRIC = 'eps'


class PER(Metric):
    METRIC = 'per'


class BPS(Metric):
    METRIC = 'bps'


class PBR(Metric):
    METRIC = 'pbr'


class ROE(Metric):
    METRIC = 'roe'


class ROA(Metric):
    METRIC = 'roa'


class SPS(Metric):
    METRIC = 'sps'


class PSR(Metric):
    METRIC = 'psr'


class CPS(Metric):
    METRIC = 'cps'


class PCR(Metric):
    METRIC = 'pcr'


class Combo4(Metric):
    METRIC = 'combo_4'


class EV_EVITDA(Metric):
    METRIC = 'ev_evitda'


class EV_Sales(Metric):
    METRIC = 'ev_sales'


class NCAV(Metric):
    METRIC = 'ncav'


class PEG(Metric):
    METRIC = 'peg'


class GP_A(Metric):
    METRIC = 'gp_a'


class DebtRatio(Metric):
    METRIC = 'debt_ratio'


class BorrowRatio(Metric):
    METRIC = 'borrow_ratio'


class RevenueGrowth(Metric):
    METRIC = 'revenue_growth'


class OperIncomeGrowth(Metric):
    METRIC = 'oper_income_growth'


class AssetTurnover(Metric):
    METRIC = 'asset_turnover'


class TradeReceiveTurnover(Metric):
    METRIC = 'trade_receive_turnover'


class InventoryTurnover(Metric):
    METRIC = 'inventory_turnover'


class GrossMargin(Metric):
    METRIC = 'gorss_margin'


class OperMargin(Metric):
    METRIC = 'oper_margin'


class ProfitMargin(Metric):
    METRIC = 'profit_margin'
