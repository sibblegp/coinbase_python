__author__ = 'gsibble'

from decimal import Decimal


SATOSHIS_IN_A_BITCOIN = Decimal('100,000,000'.replace(',',''))


class CoinbaseAmount(Decimal):

    @classmethod
    def from_coinbase_dict(cls, a):
        if 'amount' in a:
            return CoinbaseAmount(a['amount'], a['currency'])
        elif 'cents' in a:
            currency = a['currency_iso']
            amount = a['cents'] / (SATOSHIS_IN_A_BITCOIN if currency == 'BTC'
                                   else Decimal('100'))
            return CoinbaseAmount(amount, currency)
        else:
            raise Exception

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
