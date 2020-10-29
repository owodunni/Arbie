"""Utility functions for createting large numbers."""


class BigNumber(object):
    """BigNumber is used for creating etheruem friendly numbers."""

    def __init__(self, value, exp=18):
        self.value = int(round(value * 10 ** exp))
        self.exp = exp

    def __eq__(self, other):
        if isinstance(other, BigNumber):
            return self.value == other.value and self.exp == other.exp
        return self.value == other

    @classmethod
    def from_value(cls, value, exp=18):
        bg = cls(0, exp)
        bg.value = value
        return bg

    def to_number(self):
        return int(round(self.value / (10 ** self.exp)))
