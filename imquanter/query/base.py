from copy import deepcopy
from abc import ABCMeta, abstractmethod


class Query(metaclass=ABCMeta):
    """Query Interface"""

    @property
    def query(self):
        return None

    @property
    def query_str(self):
        if not hasattr(self, 'connection'):
            result = self.query
        else:
            result = str(self.connection)
        result = result.replace(",", "")
        result = result.replace("[", "(")
        result = result.replace("]", ")")
        return result

    def __str__(self):
        return self.query_str

    def __repr__(self):
        return self.query_str

    def _combine(self, other, conn):
        if not hasattr(self, 'connection'):
            self.connection = [deepcopy(self)]

        if hasattr(other, 'connection'):
            target = other.connection
        else:
            target = other
        self.connection.append(conn)
        self.connection.append(target)
        return self

    def __and__(self, other):
        return self._combine(other, AND())

    def __or__(self, other):
        return self._combine(other, OR())


class Generic(Query):
    QUERY_TYPE = 'all'


class AND(Generic):
    @property
    def query(self):
        return "AND"


class OR(Generic):
    @property
    def query(self):
        return "OR"


class Factor(Query):
    QUERY_TYPE = 'factor'


class Statement(Query):
    QUERY_TYPE = 'statement'


class Price(Query):
    QUERY_TYPE = 'price'


def is_query(target):
    return target.__class__.__bases__[0] is Query


if __name__ == '__main__':
    pass