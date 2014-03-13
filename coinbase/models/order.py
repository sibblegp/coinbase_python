__author__ = 'vkhougaz'

from amount import CoinbaseAmount
from button import CoinbaseButton
from transaction import CoinbaseTransaction
# from datetime import datetime

class CoinbaseOrder(object):
    def __init__(self, order):
        self.data = order

        self.order_id = order['id']
        # TODO: Account for timezone properly
        #self.created_at = datetime.strptime(order['created_at'], '%Y-%m-%dT%H:%M:%S-08:00')
        self.created_at = order['created_at']
        self.status = order['status']
        self.custom = order['custom']

        btc_cents = order['total_btc']['cents']
        btc_currency_iso = order['total_btc']['currency_iso']
        self.total_btc = CoinbaseAmount.from_cents(btc_cents, btc_currency_iso)

        native_cents = order['total_native']['cents']
        native_currency_iso = order['total_native']['currency_iso']
        self.total_native = CoinbaseAmount.from_cents(native_cents, native_currency_iso)

        self.button = CoinbaseButton(order['button'])
        if 'transaction' in order and order['transaction'] is not None:
            self.transaction = CoinbaseTransaction(order['transaction'])
        else:
            self.transaction = None
