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
        if self.gte:
            strings.append(f"{self.gte} <= {self.METRIC}")
        if self.lte:
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