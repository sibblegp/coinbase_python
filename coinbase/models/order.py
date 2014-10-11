import dateutil.parser
from enum import Enum
import json

from .util import namedtuple, optional
from . import CoinbaseAmount


class CoinbaseOrder(namedtuple(
    'CoinbaseOrder',
    optional='id created_at status receive_address button '
             'transaction custom total mispaid customer refund_address'
)):
    """
    Orders are be created through the API, or by a user clicking a
    payment button. In the latter case, the order is only behind
    the scenes; it is hidden from the API until a payment is made.

    status
            CoinbaseOrder.Status
    total
            CoinbaseAmount.BtcAndNative. This is the order's price; in other
            words, the amount that Coinbase expects to receive for the order's
            status to become `complete`.
    mispaid
            CoinbaseAmount.BtcAndNative. This field is present if the order's
            status is `mispaid` or `expired`. Its value is the amount of the
            most recent payment made on this order.
    refund_address
            A refund address on off-blockchain order payments.
            "This is an experimental feature."
    button
            CoinbaseOrder.Button
    transaction
            CoinbaseOrder.Transaction
    customer
            CoinbaseOrder.Customer
    """

    class Status(Enum):
        """
        Enumeration of values for `CoinbaseOrder.status`.
        """

        """
        All orders have an initial status of `pending`.
        """
        pending = 'new'

        """
        When a `pending` order receives a payment in the correct amount,
        its status permanently becomes `complete`.
        """
        complete = 'completed'

        """
        When a `pending` order receives a payment in an incorrect amount,
        its status permanently becomes `mispaid`.
        """
        mispaid = 'mispaid'

        """
        When a `pending` order's time runs out, its status permanently
        becomes `expired`.
        """
        expired = 'expired'

    @classmethod
    def parse_callback(cls, s):
        return CoinbaseOrder.from_coinbase_dict(json.loads(s))

    def render_callback(self):
        return json.dumps(self.to_coinbase_dict())

    @classmethod
    def from_coinbase_dict(cls, x):

        return CoinbaseOrder(
            id=x['order']['id'],
            created_at=dateutil.parser.parse(
                x['order']['created_at']),
            status=CoinbaseOrder.Status(x['order']['status']),
            receive_address=x['order']['receive_address'],
            button=CoinbaseOrder.Button.from_coinbase_dict(
                x['order']['button']),
            transaction=optional(CoinbaseOrder.Transaction.from_coinbase_dict)(
                x['order']['transaction']),
            custom=x['order'].get('custom'),
            total=CoinbaseAmount.BtcAndNative.from_coinbase_dict(
                x['order'], prefix='total'),
            mispaid=CoinbaseAmount.BtcAndNative.from_coinbase_dict(
                x['order'], prefix='mispaid'),
            customer=optional(CoinbaseOrder.Customer.from_coinbase_dict)(
                x.get('customer')),
            refund_address=x['order'].get('refund_address'),
        )

    def to_coinbase_dict(self):
        x = {
            'order': {
                'id': self.id,
                'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
                'status': self.status.value,
                'total_btc': self.total.btc.to_coinbase_dict(),
                'total_native': self.total.native.to_coinbase_dict(),
                'custom': self.custom,
                'receive_address': self.receive_address,
                'button': self.button.to_coinbase_dict(),
            }
        }
        if self.transaction is not None:
            x['order']['transaction'] = self.transaction.to_coinbase_dict()
        if self.customer is not None:
            x['customer'] = self.customer.to_coinbase_dict()
        return x

    class Button(namedtuple(
        'CoinbaseOrder_Button',
        'id type',
        optional='name description'
    )):

        @classmethod
        def from_coinbase_dict(cls, x):
            kwargs = {}
            for key in ['id', 'type', 'name', 'description']:
                kwargs[key] = x[key]
            return CoinbaseOrder.Button(**kwargs)

        def to_coinbase_dict(self):
            x = {}
            for key in ['id', 'type', 'name', 'description']:
                x[key] = getattr(self, key) or ''
            return x

        @classmethod
        def from_coinbase_payment_button(cls, button):
            """
            button - CoinbasePaymentButton
            """
            kwargs = {}
            for key in ['id', 'type', 'name', 'description']:
                kwargs[key] = getattr(button, key) or ''
            return CoinbaseOrder.Button(**kwargs)

    class Transaction(namedtuple(
        'CoinbaseOrder_Transaction',
        'id hash confirmations'
    )):

        @classmethod
        def from_coinbase_dict(cls, x):
            kwargs = {}
            for key in ['id', 'hash', 'confirmations']:
                kwargs[key] = x[key]
            return CoinbaseOrder.Transaction(**kwargs)

        def to_coinbase_dict(self):
            x = {}
            for key in ['id', 'hash', 'confirmations']:
                x[key] = getattr(self, key)
            return x

    class Customer(namedtuple(
        'CoinbaseOrder_Customer',
        optional='email shipping_address'
    )):

        @classmethod
        def from_coinbase_dict(cls, x):
            kwargs = {}
            for key in ['email', 'shipping_address']:
                kwargs[key] = x.get(key)
            return CoinbaseOrder.Customer(**kwargs)

        def to_coinbase_dict(self):
            x = {}
            for key in ['email', 'shipping_address']:
                value = getattr(self, key)
                if value is not None:
                    x[key] = value
            return x
