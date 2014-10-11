from sure import this
from decimal import Decimal
from coinbase.models import CoinbaseAmount


def test_amount():
    this(CoinbaseAmount('1.063', 'BTC').amount).should.equal(Decimal('1.063'))


def test_currency():
    this(CoinbaseAmount('1.063', 'BTC').currency).should.equal('BTC')


def test_str_or_decimal():
    this(CoinbaseAmount(Decimal('1.063'), 'BTC')) \
        .should.equal(CoinbaseAmount('1.063', 'BTC'))
