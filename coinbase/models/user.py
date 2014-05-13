__author__ = 'gsibble'

from .util import namedtuple

from .amount import CoinbaseAmount


class CoinbaseUser(namedtuple(
    'CoinbaseUser',
    optional='id name email time_zone native_currency balance '
             'buy_level sell_level buy_limit sell_limit'
)):

    @classmethod
    def from_coinbase_dict(cls, user):
        return CoinbaseUser(
            id=user['id'],
            name=user['name'],
            email=user['email'],
            time_zone=user['time_zone'],
            native_currency=user['native_currency'],
            balance=CoinbaseAmount.from_coinbase_dict(
                user['balance']),
            buy_level=user['buy_level'],
            sell_level=user['sell_level'],
            buy_limit=CoinbaseAmount.from_coinbase_dict(
                user['buy_limit']),
            sell_limit=CoinbaseAmount.from_coinbase_dict(
                user['sell_limit']),
        )
