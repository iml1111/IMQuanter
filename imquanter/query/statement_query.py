from imquanter.query.base import Statement
from imquanter.util import type_valid


class Metric(Statement):
    METRIC = None

    def __init__(
            self,
            gte: int = None,
            lte: int = None):
        self.gte = gte
        self.lte = lte

    @property
    def query(self):
        strings = []
        if self.gte is not None:
            strings.append(f"{self.gte} <= {self.METRIC}")
        if self.lte is not None:
            strings.append(f"{self.METRIC} <= {self.lte}")
        return " AND ".join(strings)


class Assets(Metric):
    METRIC = 'assets'


class Equity(Metric):
    METRIC = 'equity'


class Liability(Metric):
    METRIC = 'liability'


class Revenue(Metric):
    METRIC = 'revenue'


class SalesFlow(Metric):
    METRIC = 'sales_flow'


class Profit(Metric):
    METRIC = 'profit'


class Stock(Metric):
    METRIC = 'total_stock'


class NetDebt(Metric):
    METRIC = 'net_debt'


class CurAssets(Metric):
    METRIC = 'cur_assets'


class GrossProfit(Metric):
    METRIC = 'gross_profit'


class OperIncome(Metric):
    METRIC = 'oper_income'
