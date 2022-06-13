from imquanter.query.base import Generic
from imquanter.util import type_valid


class StrMetric(Generic):
    METRIC = None

    def __init__(
            self,
            gte: str = None,
            lte: str = None,
            eq: str = None):
        self.gte = str(gte)
        self.lte = str(lte)
        if eq:
            self.gte = self.lte = str(eq)
        if gte and not lte and not eq:
            self.lte = self.gte

    @property
    def query(self):
        strings = []
        if self.gte:
            strings.append(
                f'"{self.gte}" <= {self.METRIC}')
        if self.lte:
            strings.append(
                f'{self.METRIC} <= "{self.lte}"')
        return f'({" AND ".join(strings)})'


class Year(StrMetric):
    METRIC = "f.year"


class Quarter(StrMetric):
    METRIC = "f.quarter"