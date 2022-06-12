from abc import ABCMeta, abstractmethod


class Query(metaclass=ABCMeta):
    """Query Interface"""
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    default = AND
    conditional = True

    def __init__(self, *args, **kwargs):
        pass

    def _combine(self):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __invert__(self):
        pass

    @abstractmethod
    def valid(self):
        pass


def is_query(target):
    return target.__class__.__bases__[0] is Query