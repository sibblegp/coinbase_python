__author__ = 'gsibble'

from decimal import Decimal


class CoinbaseAmount(Decimal):

    @classmethod
    def from_coinbase_dict(cls, a):
        return CoinbaseAmount(
            amount=a['amount'],
            currency=a['currency'],
        )

    def __new__(cls, amount, currency):
        return Decimal.__new__(cls, amount)

    def __init__(self, amount, currency):
        super(CoinbaseAmount, self).__init__()
        self.currency = currency

    def __repr__(self):
        return "CoinbaseAmount('%s', '%s')" % (
            str(Decimal(self)),
            self.currency,
        )

    def __unicode__(self):
        return '%s %s' % (
            str(Decimal(self)),
            self.currency,
        )

    def __str__(self):
        return self.__unicode__()

    def __eq__(self, other, context=None):
        return super(CoinbaseAmount, self).__eq__(other, context) \
            and self.currency == other.currency

    def __neq__(self, other, context=None):
        return not self.__eq__(other)
