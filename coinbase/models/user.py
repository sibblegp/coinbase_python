__author__ = 'gsibble'

from .amount import CoinbaseAmount


class CoinbaseUser(object):

    def __init__(self, user_id, name, email, time_zone, native_currency,
                 balance, buy_level, sell_level, buy_limit, sell_limit):
        self.id = user_id
        self.name = name
        self.email = email
        self.time_zone = time_zone
        self.native_currency = native_currency
        self.balance = balance
        self.buy_level = buy_level
        self.sell_level = sell_level
        self.buy_limit = buy_limit
        self.sell_limit = sell_limit

    @classmethod
    def from_coinbase_dict(cls, user):
        return CoinbaseUser(
            user_id=user['id'],
            name=user['name'],
            email=user['email'],
            time_zone=user['time_zone'],
            native_currency=user['native_currency'],
            balance=CoinbaseAmount.from_coinbase_dict(user['balance']),
            buy_level=user['buy_level'],
            sell_level=user['sell_level'],
            buy_limit=CoinbaseAmount.from_coinbase_dict(user['buy_limit']),
            sell_limit=CoinbaseAmount.from_coinbase_dict(user['sell_limit']),
        )
