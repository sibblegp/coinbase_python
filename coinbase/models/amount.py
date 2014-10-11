from decimal import Decimal

from .util import namedtuple

SATOSHIS_IN_A_BITCOIN = Decimal('100,000,000'.replace(',', ''))


class CoinbaseAmount(namedtuple(
    'CoinbaseAmount',
    'amount currency'
)):

    def __new__(cls, amount, currency):
        return super(CoinbaseAmount, cls).__new__(
            cls,
            Decimal(amount),
            currency,
        )

    @classmethod
    def from_coinbase_dict(cls, x):
        if 'amount' in x:
            return CoinbaseAmount(x['amount'], x['currency'])
        elif 'cents' in x:
            currency = x['currency_iso']
            amount = x['cents'] / (SATOSHIS_IN_A_BITCOIN if currency == 'BTC'
                                   else Decimal('100'))
            return CoinbaseAmount(amount, currency)
        else:
            raise Exception

    def to_coinbase_dict(self):
        return {
            'amount': str(self.amount),
            'currency': self.currency,
        }

    def convert(self, currency, exchange_rate):
        return CoinbaseAmount(self.amount * exchange_rate, currency)

    class BtcAndNative(namedtuple('CoinbaseAmount_BtcAndNative', 'btc native')):

        @classmethod
        def from_coinbase_dict(cls, x, prefix):

            btc_key = prefix + '_btc'
            native_key = prefix + '_native'

            if btc_key not in x:
                return None

            return CoinbaseAmount.BtcAndNative(
                btc=CoinbaseAmount.from_coinbase_dict(x[btc_key]),
                native=CoinbaseAmount.from_coinbase_dict(x[native_key])
            )
