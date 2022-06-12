from imquanter.query.base import Generic
from imquanter.util import type_valid


class StrMetric(Generic):
    METRIC = None

    def __init__(
            self,
            gte: str = None,
            lte: str = None):
        type_valid(gte, str)
        type_valid(lte, str)
        self.gte = gte
        self.lte = lte

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