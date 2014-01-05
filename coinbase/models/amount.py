__author__ = 'gsibble'

from decimal import Decimal

class CoinbaseAmount(Decimal):

    def __new__(self, amount, currency):
        return Decimal.__new__(self, amount)

    def __init__(self, amount, currency):
        super(CoinbaseAmount, self).__init__()
        self.currency = currency

    def __eq__(self, other, *args, **kwargs):
        if isinstance(other, self.__class__) and self.currency != other.currency:
            return False
        return super(CoinbaseAmount, self).__eq__(other, *args, **kwargs)