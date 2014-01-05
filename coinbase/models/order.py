__author__ = 'vkhougaz'

from amount import CoinbaseAmount
from button import CoinbaseButton
from transaction import CoinbaseTransaction
from decimal import Decimal
from coinbase.config import CENTS_PER_BITCOIN, CENTS_PER_OTHER
# from datetime import datetime

class CoinbaseOrder(object):
    def __init__(self, order):
        self.id = order['id']
        # TODO: Account for timezone properly
        #self.created_at = datetime.strptime(order['created_at'], '%Y-%m-%dT%H:%M:%S-08:00')
        self.created_at = order['created_at']
        self.status = order['status']
        self.custom = order['custom']

        btc_cents = Decimal(order['total_btc']['cents'])
        btc_currency_iso = order['total_btc']['currency_iso']
        if btc_currency_iso == 'BTC':
            btc_cents /= CENTS_PER_BITCOIN
        else:
            btc_cents /= CENTS_PER_OTHER
        self.total_btc = CoinbaseAmount(btc_cents, btc_currency_iso)

        native_cents = order['total_native']['cents']
        native_currency_iso = order['total_native']['currency_iso']
        if native_currency_iso == 'BTC':
            native_cents /= CENTS_PER_BITCOIN
        else:
            native_cents /= CENTS_PER_OTHER
        self.total_native = CoinbaseAmount(native_cents, native_currency_iso)

        self.button = CoinbaseButton(order['button'])
        if 'transaction' in order and order['transaction'] is not None:
            self.transaction = CoinbaseTransaction(order['transaction'])
        else:
            self.transaction = None
